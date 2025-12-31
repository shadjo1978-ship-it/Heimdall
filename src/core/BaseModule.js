/**
 * Base Module Interface
 * All modules should extend this class
 */

class BaseModule {
  constructor(application, config = {}) {
    this.application = application;
    this.config = config;
    this.logger = application.logger;
    this.name = this.constructor.name;
  }

  /**
   * Initialize the module
   * Override this method to perform setup
   */
  async initialize() {
    this.logger.debug(`Initializing ${this.name}`);
  }

  /**
   * Start the module
   * Override this method to start services
   */
  async start() {
    this.logger.debug(`Starting ${this.name}`);
  }

  /**
   * Stop the module
   * Override this method to cleanup
   */
  async stop() {
    this.logger.debug(`Stopping ${this.name}`);
  }

  /**
   * Get configuration value
   */
  getConfig(key, defaultValue) {
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
}

module.exports = BaseModule;
