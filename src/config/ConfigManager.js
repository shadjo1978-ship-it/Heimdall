/**
 * Configuration Manager
 * Handles application configuration loading and management
 */

const fs = require('fs').promises;
const path = require('path');
const yaml = require('js-yaml');

class ConfigManager {
  constructor(configPath) {
    this.configPath = configPath;
    this.config = {};
    this.env = process.env.NODE_ENV || 'development';
  }

  /**
   * Load configuration from file
   */
  async load() {
    try {
      // Check if config file exists
      const fullPath = path.resolve(this.configPath);
      const content = await fs.readFile(fullPath, 'utf8');
      
      // Parse based on file extension
      if (fullPath.endsWith('.yaml') || fullPath.endsWith('.yml')) {
        this.config = yaml.load(content);
      } else if (fullPath.endsWith('.json')) {
        this.config = JSON.parse(content);
      } else {
        throw new Error('Unsupported configuration file format');
      }

      // Merge with environment variables
      this.mergeEnvVariables();

      return this.config;
    } catch (error) {
      if (error.code === 'ENOENT') {
        console.warn(`Configuration file not found: ${this.configPath}, using defaults`);
        this.loadDefaults();
      } else {
        throw new Error(`Failed to load configuration: ${error.message}`);
      }
    }
  }

  /**
   * Load default configuration
   */
  loadDefaults() {
    this.config = {
      environment: this.env,
      logging: {
        level: 'info',
        format: 'json'
      },
      modules: {
        storage: { enabled: true },
        firewall: { enabled: true },
        ai: { enabled: true },
        voice: { enabled: false },
        api: { enabled: true }
      }
    };
  }

  /**
   * Merge environment variables with config
   */
  mergeEnvVariables() {
    // Override with environment variables (HEIMDALL_ prefix)
    const envPrefix = 'HEIMDALL_';
    
    for (const [key, value] of Object.entries(process.env)) {
      if (key.startsWith(envPrefix)) {
        const configKey = key.substring(envPrefix.length).toLowerCase().replace(/_/g, '.');
        this.set(configKey, value);
      }
    }
  }

  /**
   * Get configuration value
   */
  get(key, defaultValue) {
    const keys = key.split('.');
    let value = this.config;

    for (const k of keys) {
      if (value && typeof value === 'object' && k in value) {
        value = value[k];
      } else {
        return defaultValue;
      }
    }

    return value !== undefined ? value : defaultValue;
  }

  /**
   * Set configuration value
   */
  set(key, value) {
    const keys = key.split('.');
    let obj = this.config;

    for (let i = 0; i < keys.length - 1; i++) {
      const k = keys[i];
      if (!(k in obj) || typeof obj[k] !== 'object') {
        obj[k] = {};
      }
      obj = obj[k];
    }

    obj[keys[keys.length - 1]] = value;
  }

  /**
   * Get all configuration
   */
  getAll() {
    return { ...this.config };
  }
}

module.exports = ConfigManager;
