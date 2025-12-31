/**
 * Storage Module
 * Handles data persistence and caching
 */

const BaseModule = require('../core/BaseModule');

class StorageModule extends BaseModule {
  constructor(application, config) {
    super(application, config);
    this.database = null;
    this.cache = null;
  }

  async initialize() {
    await super.initialize();
    
    this.logger.info('Initializing Storage module');

    // Initialize database connection
    const dbType = this.getConfig('database.type', 'memory');
    this.database = this.createDatabase(dbType);

    // Initialize cache
    if (this.getConfig('cache.enabled', true)) {
      this.cache = this.createCache();
    }
  }

  /**
   * Create database connection
   */
  createDatabase(type) {
    // Placeholder for actual database implementation
    return new InMemoryDatabase();
  }

  /**
   * Create cache
   */
  createCache() {
    const ttl = this.getConfig('cache.ttl', 300);
    return new InMemoryCache(ttl);
  }

  /**
   * Store data
   */
  async set(key, value, options = {}) {
    try {
      await this.database.set(key, value);
      
      // Also cache if enabled
      if (this.cache && options.cache !== false) {
        this.cache.set(key, value);
      }
      
      return true;
    } catch (error) {
      this.logger.error('Failed to store data', error);
      throw error;
    }
  }

  /**
   * Retrieve data
   */
  async get(key) {
    try {
      // Try cache first
      if (this.cache) {
        const cached = this.cache.get(key);
        if (cached !== null) {
          return cached;
        }
      }

      // Fetch from database
      const value = await this.database.get(key);
      
      // Update cache
      if (this.cache && value !== null) {
        this.cache.set(key, value);
      }

      return value;
    } catch (error) {
      this.logger.error('Failed to retrieve data', error);
      throw error;
    }
  }

  /**
   * Delete data
   */
  async delete(key) {
    try {
      if (this.cache) {
        this.cache.delete(key);
      }
      await this.database.delete(key);
      return true;
    } catch (error) {
      this.logger.error('Failed to delete data', error);
      throw error;
    }
  }

  /**
   * Query data
   */
  async query(filter) {
    try {
      return await this.database.query(filter);
    } catch (error) {
      this.logger.error('Failed to query data', error);
      throw error;
    }
  }
}

/**
 * In-Memory Database (placeholder)
 */
class InMemoryDatabase {
  constructor() {
    this.data = new Map();
  }

  async set(key, value) {
    this.data.set(key, value);
  }

  async get(key) {
    return this.data.get(key) || null;
  }

  async delete(key) {
    this.data.delete(key);
  }

  async query(filter) {
    // Simple filter implementation
    const results = [];
    for (const [key, value] of this.data.entries()) {
      if (this.matchesFilter(value, filter)) {
        results.push({ key, value });
      }
    }
    return results;
  }

  matchesFilter(value, filter) {
    if (!filter) return true;
    
    for (const [key, filterValue] of Object.entries(filter)) {
      if (value[key] !== filterValue) {
        return false;
      }
    }
    return true;
  }
}

/**
 * In-Memory Cache
 */
class InMemoryCache {
  constructor(ttl = 300) {
    this.cache = new Map();
    this.ttl = ttl * 1000; // Convert to milliseconds
  }

  set(key, value) {
    this.cache.set(key, {
      value,
      expiry: Date.now() + this.ttl
    });
  }

  get(key) {
    const item = this.cache.get(key);
    
    if (!item) {
      return null;
    }

    if (Date.now() > item.expiry) {
      this.cache.delete(key);
      return null;
    }

    return item.value;
  }

  delete(key) {
    this.cache.delete(key);
  }

  clear() {
    this.cache.clear();
  }
}

module.exports = StorageModule;
