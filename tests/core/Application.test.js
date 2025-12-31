/**
 * Core Application Tests
 */

const Application = require('../../src/core/Application');

describe('Application', () => {
  let app;

  beforeEach(() => {
    app = new Application();
  });

  afterEach(async () => {
    if (app.isRunning) {
      await app.stop();
    }
  });

  describe('initialization', () => {
    test('should create application instance', () => {
      expect(app).toBeInstanceOf(Application);
      expect(app.isRunning).toBe(false);
    });

    test('should initialize with default config path', () => {
      expect(app.configPath).toBe('./config/config.yaml');
    });

    test('should initialize with custom config path', () => {
      const customApp = new Application('/custom/path/config.yaml');
      expect(customApp.configPath).toBe('/custom/path/config.yaml');
    });
  });

  describe('module management', () => {
    test('should have module registry after initialization', async () => {
      await app.initialize();
      expect(app.moduleRegistry).toBeDefined();
    });

    test('should register core modules', async () => {
      await app.initialize();
      const moduleNames = app.moduleRegistry.getModuleNames();
      expect(moduleNames.length).toBeGreaterThan(0);
    });

    test('should get module by name', async () => {
      await app.initialize();
      const storage = app.getModule('storage');
      expect(storage).toBeDefined();
    });
  });

  describe('lifecycle', () => {
    test('should start and stop successfully', async () => {
      await app.initialize();
      await app.start();
      expect(app.isRunning).toBe(true);
      
      await app.stop();
      expect(app.isRunning).toBe(false);
    });

    test('should emit events on lifecycle changes', async () => {
      const events = [];
      app.on('initialized', () => events.push('initialized'));
      app.on('started', () => events.push('started'));
      app.on('stopped', () => events.push('stopped'));

      await app.initialize();
      await app.start();
      await app.stop();

      expect(events).toEqual(['initialized', 'started', 'stopped']);
    });
  });
});
