/**
 * Logger
 * Structured logging system
 */

const winston = require('winston');

class Logger {
  constructor(config = {}) {
    this.config = {
      level: config.level || 'info',
      format: config.format || 'json',
      ...config
    };

    this.logger = this.createLogger();
  }

  /**
   * Create Winston logger instance
   */
  createLogger() {
    const formats = [];

    // Add timestamp
    formats.push(winston.format.timestamp());

    // Add format based on config
    if (this.config.format === 'json') {
      formats.push(winston.format.json());
    } else {
      formats.push(
        winston.format.colorize(),
        winston.format.printf(({ level, message, timestamp, ...meta }) => {
          let log = `${timestamp} [${level}]: ${message}`;
          if (Object.keys(meta).length > 0) {
            log += ` ${JSON.stringify(meta)}`;
          }
          return log;
        })
      );
    }

    return winston.createLogger({
      level: this.config.level,
      format: winston.format.combine(...formats),
      transports: [
        new winston.transports.Console(),
        // Add file transport if configured
        ...(this.config.file ? [
          new winston.transports.File({ filename: this.config.file })
        ] : [])
      ]
    });
  }

  /**
   * Log methods
   */
  debug(message, meta = {}) {
    this.logger.debug(message, meta);
  }

  info(message, meta = {}) {
    this.logger.info(message, meta);
  }

  warn(message, meta = {}) {
    this.logger.warn(message, meta);
  }

  error(message, error = null) {
    if (error instanceof Error) {
      this.logger.error(message, {
        error: error.message,
        stack: error.stack
      });
    } else {
      this.logger.error(message, error || {});
    }
  }
}

module.exports = Logger;
