/**
 * Heimdall - AI Personal Assistant
 * Main entry point
 */

const Application = require('./core/Application');

async function main() {
  const app = new Application();

  // Handle graceful shutdown
  process.on('SIGTERM', () => app.shutdown());
  process.on('SIGINT', () => app.shutdown());

  // Handle uncaught errors
  process.on('uncaughtException', (error) => {
    console.error('Uncaught exception:', error);
    app.shutdown();
  });

  process.on('unhandledRejection', (reason, promise) => {
    console.error('Unhandled rejection at:', promise, 'reason:', reason);
  });

  try {
    // Initialize and start
    await app.initialize();
    await app.start();

    console.log('Heimdall is running. Press Ctrl+C to stop.');
  } catch (error) {
    console.error('Failed to start Heimdall:', error);
    process.exit(1);
  }
}

// Run if executed directly
if (require.main === module) {
  main();
}

module.exports = { Application };
