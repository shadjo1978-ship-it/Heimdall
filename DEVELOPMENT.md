# Development Guide

## Prerequisites

- Node.js 18+ or Python 3.10+
- Docker (optional, for containerized services)
- Git

## Project Structure

```
Heimdall/
├── src/
│   ├── core/           # Core application logic
│   ├── ai/             # AI and LLM integration
│   ├── voice/          # Voice processing (STT/TTS)
│   ├── firewall/       # Security and firewall
│   ├── api/            # API endpoints
│   ├── storage/        # Data persistence
│   ├── config/         # Configuration management
│   └── monitoring/     # Logging and metrics
├── tests/              # Test suites
├── docs/               # Documentation
├── config/             # Configuration files
└── scripts/            # Utility scripts
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/shadjo1978-ship-it/Heimdall.git
cd Heimdall
```

### 2. Install Dependencies

**For Node.js:**
```bash
npm install
```

**For Python:**
```bash
pip install -r requirements.txt
```

### 3. Configuration

Copy the example configuration:
```bash
cp config/config.example.yaml config/config.yaml
```

Edit `config/config.yaml` with your settings:
- API keys for LLM providers
- Voice service credentials
- Database connection strings
- Security settings

### 4. Environment Variables

Create a `.env` file:
```bash
cp .env.example .env
```

Required environment variables:
- `NODE_ENV` or `PYTHON_ENV`: development/production
- `PORT`: Application port (default: 3000)
- `LOG_LEVEL`: debug/info/warn/error

## Running the Application

### Development Mode

**Node.js:**
```bash
npm run dev
```

**Python:**
```bash
python -m src.main
```

### Production Mode

```bash
npm start  # or python -m src.main --production
```

## Testing

### Run All Tests
```bash
npm test  # or pytest
```

### Run Specific Test Suite
```bash
npm test -- tests/core  # or pytest tests/core
```

### Coverage Report
```bash
npm run test:coverage  # or pytest --cov
```

## Code Style

### Linting
```bash
npm run lint  # or flake8/black
```

### Formatting
```bash
npm run format  # or black src/
```

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture documentation.

## Module Development

### Creating a New Module

1. Create module directory in `src/`
2. Implement module interface
3. Register in core module system
4. Add configuration schema
5. Write tests
6. Update documentation

### Example Module Structure

```javascript
// src/mymodule/index.js
class MyModule {
  constructor(config) {
    this.config = config;
  }

  async initialize() {
    // Setup logic
  }

  async shutdown() {
    // Cleanup logic
  }
}

module.exports = MyModule;
```

## Debugging

### Enable Debug Logging
```bash
DEBUG=heimdall:* npm run dev
```

### Using Debugger
```bash
node --inspect src/index.js
```

## Contributing

1. Create a feature branch
2. Make changes with tests
3. Run linting and tests
4. Submit pull request

## Common Issues

### Module Not Found
- Ensure all dependencies are installed
- Check import paths

### API Connection Errors
- Verify API keys in configuration
- Check network connectivity
- Review firewall settings

### Database Connection Issues
- Ensure database is running
- Verify connection string
- Check credentials

## Resources

- [Architecture Documentation](ARCHITECTURE.md)
- [API Documentation](docs/API.md)
- [Security Best Practices](docs/SECURITY.md)

## Support

For issues and questions, please open a GitHub issue.
