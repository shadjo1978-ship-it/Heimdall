/**
 * API Module
 * Handles REST API and WebSocket endpoints
 */

const BaseModule = require('../core/BaseModule');
const express = require('express');
const http = require('http');
const { Server } = require('socket.io');

class APIModule extends BaseModule {
  constructor(application, config) {
    super(application, config);
    this.app = null;
    this.server = null;
    this.io = null;
    this.port = this.getConfig('port', 3000);
  }

  async initialize() {
    await super.initialize();
    
    this.logger.info('Initializing API module');

    // Create Express app
    this.app = express();
    
    // Middleware
    this.app.use(express.json());
    this.app.use(express.urlencoded({ extended: true }));

    // Setup routes
    this.setupRoutes();

    // Create HTTP server
    this.server = http.createServer(this.app);

    // Initialize WebSocket if enabled
    if (this.getConfig('websocket.enabled', true)) {
      this.setupWebSocket();
    }
  }

  /**
   * Setup API routes
   */
  setupRoutes() {
    // Health check
    this.app.get('/health', (req, res) => {
      res.json({ status: 'healthy', timestamp: Date.now() });
    });

    // Process message endpoint
    this.app.post('/api/message', async (req, res) => {
      try {
        const { userId, message } = req.body;

        if (!message) {
          return res.status(400).json({ error: 'Message is required' });
        }

        // Validate with firewall
        const firewall = this.application.getModule('firewall');
        if (firewall) {
          const validation = await firewall.validateRequest({
            source: req.ip,
            content: message,
            userId
          });

          if (!validation.allowed) {
            return res.status(403).json({ 
              error: 'Request blocked',
              reason: validation.reason 
            });
          }
        }

        // Process with AI module
        const ai = this.application.getModule('ai');
        if (!ai) {
          return res.status(503).json({ error: 'AI module not available' });
        }

        const response = await ai.processMessage(userId || 'anonymous', message);
        
        res.json({ response: response.content });
      } catch (error) {
        this.logger.error('API error', error);
        res.status(500).json({ error: 'Internal server error' });
      }
    });

    // Voice input endpoint
    this.app.post('/api/voice', async (req, res) => {
      try {
        const voice = this.application.getModule('voice');
        
        if (!voice) {
          return res.status(503).json({ error: 'Voice module not available' });
        }

        // Placeholder for voice processing
        res.json({ message: 'Voice processing not yet implemented' });
      } catch (error) {
        this.logger.error('Voice API error', error);
        res.status(500).json({ error: 'Internal server error' });
      }
    });
  }

  /**
   * Setup WebSocket
   */
  setupWebSocket() {
    this.io = new Server(this.server, {
      cors: this.getConfig('websocket.cors', {
        origin: '*',
        methods: ['GET', 'POST']
      })
    });

    this.io.on('connection', (socket) => {
      this.logger.info('WebSocket client connected', { id: socket.id });

      socket.on('message', async (data) => {
        try {
          const { userId, message } = data;

          // Process message
          const ai = this.application.getModule('ai');
          if (ai) {
            const response = await ai.processMessage(
              userId || socket.id, 
              message
            );
            socket.emit('response', response);
          }
        } catch (error) {
          this.logger.error('WebSocket error', error);
          socket.emit('error', { message: 'Failed to process message' });
        }
      });

      socket.on('disconnect', () => {
        this.logger.info('WebSocket client disconnected', { id: socket.id });
      });
    });
  }

  /**
   * Start the API server
   */
  async start() {
    await super.start();

    return new Promise((resolve) => {
      this.server.listen(this.port, () => {
        this.logger.info(`API server listening on port ${this.port}`);
        resolve();
      });
    });
  }

  /**
   * Stop the API server
   */
  async stop() {
    await super.stop();

    if (this.io) {
      this.io.close();
    }

    return new Promise((resolve) => {
      this.server.close(() => {
        this.logger.info('API server stopped');
        resolve();
      });
    });
  }
}

module.exports = APIModule;
