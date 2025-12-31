/**
 * Core Application Class
 * Main entry point and orchestrator for Heimdall
 */

const EventEmitter = require('events');
const ConfigManager = require('../config/ConfigManager');
const Logger = require('../monitoring/Logger');
const ModuleRegistry = require('./ModuleRegistry');

class Application extends EventEmitter {
  constructor(configPath = './config/config.yaml') {
    super();
    this.configPath = configPath;
    this.config = null;
    this.logger = null;
    this.moduleRegistry = null;
    this.modules = new Map();
    this.isRunning = false;
  }

  /**
   * Initialize the application
   */
  async initialize() {
    try {
      // Load configuration
      this.config = new ConfigManager(this.configPath);
      await this.config.load();

      // Initialize logger
      this.logger = new Logger(this.config.get('logging', {}));
      this.logger.info('Initializing Heimdall...');

      // Initialize module registry
      this.moduleRegistry = new ModuleRegistry(this);

      // Register core modules
      await this.registerCoreModules();

      // Initialize all modules
      await this.initializeModules();

      this.logger.info('Heimdall initialized successfully');
      this.emit('initialized');
      
      return true;
    } catch (error) {
      if (this.logger) {
        this.logger.error('Failed to initialize application', error);
      } else {
        console.error('Failed to initialize application:', error);
      }
      throw error;
    }
  }

  /**
   * Register core modules
   */
  async registerCoreModules() {
    const modules = [
      { name: 'storage', path: '../storage' },
      { name: 'firewall', path: '../firewall' },
      { name: 'ai', path: '../ai' },
      { name: 'voice', path: '../voice' },
      { name: 'api', path: '../api' }
    ];

    for (const module of modules) {
      if (this.config.get(`modules.${module.name}.enabled`, true)) {
        await this.moduleRegistry.register(module.name, module.path);
      }
    }
  }

  /**
   * Initialize all registered modules
   */
  async initializeModules() {
    const moduleNames = this.moduleRegistry.getModuleNames();
    
    for (const moduleName of moduleNames) {
      try {
        this.logger.info(`Initializing module: ${moduleName}`);
        const module = await this.moduleRegistry.initialize(moduleName);
        this.modules.set(moduleName, module);
        this.logger.info(`Module ${moduleName} initialized`);
      } catch (error) {
        this.logger.error(`Failed to initialize module ${moduleName}`, error);
        if (this.config.get(`modules.${moduleName}.required`, false)) {
          throw error;
        }
      }
    }
  }

  /**
   * Start the application
   */
  async start() {
    if (this.isRunning) {
      this.logger.warn('Application is already running');
      return;
    }

    try {
      this.logger.info('Starting Heimdall...');

      // Start all modules
      for (const [name, module] of this.modules) {
        if (module.start) {
          this.logger.info(`Starting module: ${name}`);
          await module.start();
        }
      }

      this.isRunning = true;
      this.logger.info('Heimdall started successfully');
      this.emit('started');
    } catch (error) {
      this.logger.error('Failed to start application', error);
      throw error;
    }
  }

  /**
   * Stop the application
   */
  async stop() {
    if (!this.isRunning) {
      this.logger.warn('Application is not running');
      return;
    }

    try {
      this.logger.info('Stopping Heimdall...');

      // Stop all modules in reverse order
      const moduleNames = Array.from(this.modules.keys()).reverse();
      for (const name of moduleNames) {
        const module = this.modules.get(name);
        if (module.stop) {
          this.logger.info(`Stopping module: ${name}`);
          await module.stop();
        }
      }

      this.isRunning = false;
      this.logger.info('Heimdall stopped successfully');
      this.emit('stopped');
    } catch (error) {
      this.logger.error('Failed to stop application', error);
      throw error;
    }
  }

  /**
   * Get a module instance
   */
  getModule(name) {
    return this.modules.get(name);
  }

  /**
   * Graceful shutdown
   */
  async shutdown() {
    this.logger.info('Initiating graceful shutdown...');
    await this.stop();
    process.exit(0);
  }
}

module.exports = Application;
