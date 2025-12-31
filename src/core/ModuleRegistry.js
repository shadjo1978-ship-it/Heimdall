/**
 * Module Registry
 * Manages module lifecycle and dependencies
 */

class ModuleRegistry {
  constructor(application) {
    this.application = application;
    this.modules = new Map();
    this.instances = new Map();
  }

  /**
   * Register a module
   */
  async register(name, modulePath) {
    if (this.modules.has(name)) {
      throw new Error(`Module ${name} is already registered`);
    }

    try {
      const ModuleClass = require(modulePath);
      this.modules.set(name, {
        name,
        path: modulePath,
        ModuleClass
      });
    } catch (error) {
      throw new Error(`Failed to register module ${name}: ${error.message}`);
    }
  }

  /**
   * Initialize a module
   */
  async initialize(name) {
    if (!this.modules.has(name)) {
      throw new Error(`Module ${name} is not registered`);
    }

    if (this.instances.has(name)) {
      return this.instances.get(name);
    }

    const { ModuleClass } = this.modules.get(name);
    const config = this.application.config.get(`modules.${name}`, {});
    
    const instance = new ModuleClass(this.application, config);
    
    if (instance.initialize) {
      await instance.initialize();
    }

    this.instances.set(name, instance);
    return instance;
  }

  /**
   * Get all registered module names
   */
  getModuleNames() {
    return Array.from(this.modules.keys());
  }

  /**
   * Check if a module is registered
   */
  isRegistered(name) {
    return this.modules.has(name);
  }

  /**
   * Check if a module is initialized
   */
  isInitialized(name) {
    return this.instances.has(name);
  }
}

module.exports = ModuleRegistry;
