# Heimdall

AI personal assistant with real-time thinking and voice capabilities, featuring integrated firewall protection.

## Features

- 🤖 **AI-Powered**: Intelligent conversation with context-aware responses
- 🗣️ **Voice Interaction**: Speech-to-Text and Text-to-Speech capabilities
- 🛡️ **Built-in Firewall**: Advanced security with request filtering and threat detection
- 🔌 **Modular Architecture**: Extensible plugin system
- 🌐 **REST & WebSocket APIs**: Flexible integration options
- 📊 **Monitoring**: Built-in logging and metrics collection

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/shadjo1978-ship-it/Heimdall.git
cd Heimdall

# Install dependencies
npm install

# Set up configuration
cp config/config.example.yaml config/config.yaml
cp .env.example .env

# Start the application
npm start
```

### Usage

```bash
# Development mode with auto-reload
npm run dev

# Run tests
npm test

# Run linter
npm run lint
```

## Architecture

Heimdall is built with a modular architecture consisting of:

- **Core Module**: Application lifecycle and module orchestration
- **AI Module**: LLM integration and conversation management
- **Voice Module**: Speech-to-text and text-to-speech processing
- **Firewall Module**: Security, filtering, and threat detection
- **API Module**: REST and WebSocket endpoints
- **Storage Module**: Data persistence and caching
- **Monitoring Module**: Logging and metrics

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed documentation.

## Documentation

- [Architecture Overview](ARCHITECTURE.md)
- [Development Guide](DEVELOPMENT.md)
- [API Documentation](docs/API.md)
- [Security Best Practices](docs/SECURITY.md)

## Configuration

Configure Heimdall by editing `config/config.yaml`:

```yaml
modules:
  ai:
    enabled: true
    provider: openai
  
  voice:
    enabled: false
  
  firewall:
    enabled: true
    rateLimit:
      maxRequests: 100
      windowMs: 60000
```

## API Examples

### REST API

```bash
curl -X POST http://localhost:3000/api/message \
  -H "Content-Type: application/json" \
  -d '{"userId": "user123", "message": "Hello!"}'
```

### WebSocket

```javascript
const socket = io('http://localhost:3000');
socket.emit('message', { userId: 'user123', message: 'Hello!' });
socket.on('response', (data) => console.log(data.content));
```

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting PRs.

## License

MIT

## Support

For issues and questions, please open a GitHub issue.
