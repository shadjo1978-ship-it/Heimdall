/**
 * Firewall Module
 * Handles security, filtering, and threat detection
 */

const BaseModule = require('../core/BaseModule');

class FirewallModule extends BaseModule {
  constructor(application, config) {
    super(application, config);
    this.rules = [];
    this.rateLimiter = null;
    this.blocklist = new Set();
    this.allowlist = new Set();
  }

  async initialize() {
    await super.initialize();
    
    this.logger.info('Initializing Firewall module');

    // Load firewall rules
    this.loadRules();

    // Initialize rate limiter
    this.rateLimiter = new RateLimiter(
      this.getConfig('rateLimit.maxRequests', 100),
      this.getConfig('rateLimit.windowMs', 60000)
    );

    // Load blocklist and allowlist
    this.loadBlocklist();
    this.loadAllowlist();
  }

  /**
   * Load firewall rules
   */
  loadRules() {
    const rulesConfig = this.getConfig('rules', []);
    this.rules = rulesConfig.map(rule => ({
      id: rule.id,
      type: rule.type,
      pattern: new RegExp(rule.pattern),
      action: rule.action || 'block',
      enabled: rule.enabled !== false
    }));
    
    this.logger.info(`Loaded ${this.rules.length} firewall rules`);
  }

  /**
   * Load blocklist
   */
  loadBlocklist() {
    const blocklist = this.getConfig('blocklist', []);
    this.blocklist = new Set(blocklist);
    this.logger.info(`Loaded ${this.blocklist.size} blocked entries`);
  }

  /**
   * Load allowlist
   */
  loadAllowlist() {
    const allowlist = this.getConfig('allowlist', []);
    this.allowlist = new Set(allowlist);
    this.logger.info(`Loaded ${this.allowlist.size} allowed entries`);
  }

  /**
   * Validate incoming request
   */
  async validateRequest(request) {
    const { source, content, userId } = request;

    // Check allowlist first
    if (this.allowlist.has(source) || this.allowlist.has(userId)) {
      return { allowed: true, reason: 'allowlisted' };
    }

    // Check blocklist
    if (this.blocklist.has(source) || this.blocklist.has(userId)) {
      this.logger.warn('Request blocked by blocklist', { source, userId });
      return { allowed: false, reason: 'blocked' };
    }

    // Check rate limit
    if (!this.rateLimiter.checkLimit(userId || source)) {
      this.logger.warn('Request rate limited', { source, userId });
      return { allowed: false, reason: 'rate_limited' };
    }

    // Apply firewall rules
    for (const rule of this.rules) {
      if (!rule.enabled) continue;

      if (this.matchesRule(rule, content)) {
        this.logger.warn('Request matched firewall rule', { 
          ruleId: rule.id, 
          action: rule.action 
        });
        
        if (rule.action === 'block') {
          return { allowed: false, reason: `rule:${rule.id}` };
        }
      }
    }

    return { allowed: true };
  }

  /**
   * Check if content matches a rule
   */
  matchesRule(rule, content) {
    if (!content) return false;
    
    switch (rule.type) {
      case 'pattern':
        return rule.pattern.test(content);
      case 'keyword':
        return content.toLowerCase().includes(rule.pattern.source.toLowerCase());
      default:
        return false;
    }
  }

  /**
   * Scan content for threats
   */
  async scanContent(content) {
    // Placeholder for content scanning (malware, injection, etc.)
    const threats = [];

    // Basic XSS detection
    if (/<script|javascript:|onerror=/i.test(content)) {
      threats.push({ type: 'xss', severity: 'high' });
    }

    // Basic SQL injection detection
    if (/(\bor\b|\band\b).*=.*['"]|union\s+select/i.test(content)) {
      threats.push({ type: 'sql_injection', severity: 'high' });
    }

    if (threats.length > 0) {
      this.logger.warn('Threats detected in content', { threats });
    }

    return threats;
  }

  /**
   * Add to blocklist
   */
  block(identifier) {
    this.blocklist.add(identifier);
    this.logger.info(`Added to blocklist: ${identifier}`);
  }

  /**
   * Remove from blocklist
   */
  unblock(identifier) {
    this.blocklist.delete(identifier);
    this.logger.info(`Removed from blocklist: ${identifier}`);
  }
}

/**
 * Rate Limiter
 * Simple token bucket rate limiter
 */
class RateLimiter {
  constructor(maxRequests, windowMs) {
    this.maxRequests = maxRequests;
    this.windowMs = windowMs;
    this.requests = new Map();
  }

  checkLimit(identifier) {
    const now = Date.now();
    
    if (!this.requests.has(identifier)) {
      this.requests.set(identifier, []);
    }

    const userRequests = this.requests.get(identifier);
    
    // Remove old requests outside the window
    const validRequests = userRequests.filter(
      timestamp => now - timestamp < this.windowMs
    );

    if (validRequests.length >= this.maxRequests) {
      return false;
    }

    validRequests.push(now);
    this.requests.set(identifier, validRequests);
    return true;
  }

  reset(identifier) {
    this.requests.delete(identifier);
  }
}

module.exports = FirewallModule;
