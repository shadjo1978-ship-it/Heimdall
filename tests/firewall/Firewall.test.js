/**
 * Firewall Module Tests
 */

const FirewallModule = require('../../src/firewall');

describe('FirewallModule', () => {
  let firewall;
  let mockApp;

  beforeEach(() => {
    mockApp = {
      logger: {
        info: jest.fn(),
        warn: jest.fn(),
        error: jest.fn(),
        debug: jest.fn()
      }
    };

    const config = {
      rateLimit: {
        maxRequests: 5,
        windowMs: 1000
      },
      rules: [
        {
          id: 'test-rule',
          type: 'pattern',
          pattern: 'malicious',
          action: 'block',
          enabled: true
        }
      ],
      blocklist: ['blocked-user'],
      allowlist: ['trusted-user']
    };

    firewall = new FirewallModule(mockApp, config);
  });

  describe('initialization', () => {
    test('should initialize with config', async () => {
      await firewall.initialize();
      expect(firewall.rules.length).toBe(1);
      expect(firewall.blocklist.size).toBe(1);
      expect(firewall.allowlist.size).toBe(1);
    });
  });

  describe('request validation', () => {
    beforeEach(async () => {
      await firewall.initialize();
    });

    test('should allow valid requests', async () => {
      const result = await firewall.validateRequest({
        source: '192.168.1.1',
        content: 'Hello',
        userId: 'user123'
      });

      expect(result.allowed).toBe(true);
    });

    test('should block requests from blocklist', async () => {
      const result = await firewall.validateRequest({
        source: '192.168.1.1',
        content: 'Hello',
        userId: 'blocked-user'
      });

      expect(result.allowed).toBe(false);
      expect(result.reason).toBe('blocked');
    });

    test('should allow requests from allowlist', async () => {
      const result = await firewall.validateRequest({
        source: '192.168.1.1',
        content: 'malicious content',
        userId: 'trusted-user'
      });

      expect(result.allowed).toBe(true);
      expect(result.reason).toBe('allowlisted');
    });

    test('should block requests matching rules', async () => {
      const result = await firewall.validateRequest({
        source: '192.168.1.1',
        content: 'This is malicious',
        userId: 'user123'
      });

      expect(result.allowed).toBe(false);
      expect(result.reason).toBe('rule:test-rule');
    });

    test('should enforce rate limiting', async () => {
      const requests = [];
      const maxRequests = 5; // Matches the config
      
      // Make requests up to the limit + 1
      for (let i = 0; i < maxRequests + 1; i++) {
        const result = await firewall.validateRequest({
          source: '192.168.1.1',
          content: 'Hello',
          userId: 'user123'
        });
        requests.push(result);
      }

      // First maxRequests should be allowed
      expect(requests.slice(0, maxRequests).every(r => r.allowed)).toBe(true);
      
      // Last one should be rate limited
      expect(requests[maxRequests].allowed).toBe(false);
      expect(requests[maxRequests].reason).toBe('rate_limited');
    });
  });

  describe('content scanning', () => {
    beforeEach(async () => {
      await firewall.initialize();
    });

    test('should detect XSS attempts', async () => {
      const threats = await firewall.scanContent('<script>alert("xss")</script>');
      expect(threats.length).toBeGreaterThan(0);
      expect(threats[0].type).toBe('xss');
    });

    test('should detect SQL injection attempts', async () => {
      const threats = await firewall.scanContent("' OR 1=1 --");
      expect(threats.length).toBeGreaterThan(0);
      expect(threats[0].type).toBe('sql_injection');
    });

    test('should return empty array for safe content', async () => {
      const threats = await firewall.scanContent('Hello, this is safe content');
      expect(threats.length).toBe(0);
    });
  });

  describe('blocklist management', () => {
    beforeEach(async () => {
      await firewall.initialize();
    });

    test('should add to blocklist', () => {
      firewall.block('new-user');
      expect(firewall.blocklist.has('new-user')).toBe(true);
    });

    test('should remove from blocklist', () => {
      firewall.block('temp-user');
      expect(firewall.blocklist.has('temp-user')).toBe(true);
      
      firewall.unblock('temp-user');
      expect(firewall.blocklist.has('temp-user')).toBe(false);
    });
  });
});
