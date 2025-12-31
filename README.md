# Heimdall

A.I personal assistant with real time thinking and voice also serves as a firewall

## Overview

Heimdall is a modular AI assistant framework built with a layered architecture that supports:
- **Real-time Thinking**: AI reasoning with visible thinking steps
- **Voice Processing**: Speech-to-text and text-to-speech capabilities
- **Security/Firewall**: Built-in request validation and content filtering
- **Extensibility**: Easy to add custom layers for additional functionality

## Architecture

Heimdall uses a multi-layer architecture where each layer processes input sequentially:

1. **Security Layer** - Validates and sanitizes input, blocks malicious patterns
2. **Voice Layer** - Handles voice input/output processing
3. **Thinking Layer** - Performs AI reasoning with real-time thinking display

## Installation

```bash
pip install -r requirements.txt
```

Or install in development mode:

```bash
pip install -e .
```

## Quick Start

### Basic Usage

```python
import asyncio
from heimdall import Assistant
from heimdall.utils import get_default_config

async def main():
    # Create and initialize assistant
    config = get_default_config()
    assistant = Assistant(config)
    await assistant.initialize()
    
    # Simple chat
    response = await assistant.chat("Hello, what can you help me with?")
    print(response)
    
    # Cleanup
    await assistant.shutdown()

asyncio.run(main())
```

### Configuration

Configuration can be loaded from a YAML file or provided as a dictionary:

```yaml
# config.yml
layers:
  security:
    enabled: true
    blocked_patterns: []
    rate_limit: 100
    sanitize_input: true
  
  voice:
    enabled: true
    sample_rate: 16000
    language: en-US
  
  thinking:
    enabled: true
    model: default
    temperature: 0.7
    real_time: true
```

```python
from heimdall.utils import load_config

config = load_config('config.yml')
assistant = Assistant(config)
```

## Layers

### Security Layer

The security layer provides firewall-like functionality:
- Pattern-based blocking
- Input sanitization
- Rate limiting
- Threat detection

### Voice Layer

Handles voice-related processing:
- Speech-to-text conversion
- Text-to-speech generation
- Multi-language support
- Configurable sample rates

### Thinking Layer

Core AI reasoning engine:
- Real-time thinking steps
- Response generation
- Configurable models and temperature
- Context processing

## Custom Layers

You can extend Heimdall with custom layers:

```python
from heimdall.layers.base import BaseLayer

class CustomLayer(BaseLayer):
    async def process(self, input_data):
        # Your custom processing logic
        return processed_data

# Add to assistant
assistant = Assistant(config)
assistant.layers.append(CustomLayer())
```

## Examples

See the `examples/` directory for more examples:
- `basic_usage.py` - Basic assistant usage
- `custom_layer.py` - Creating custom layers

Run examples:

```bash
python examples/basic_usage.py
python examples/custom_layer.py
```

## API Reference

### Assistant

Main class for interacting with Heimdall:

- `__init__(config)` - Initialize with configuration
- `async initialize()` - Initialize all layers
- `async shutdown()` - Cleanup resources
- `async process(input_data)` - Process input through all layers
- `async chat(message)` - Simple chat interface

### BaseLayer

Base class for creating custom layers:

- `__init__(config)` - Initialize layer with configuration
- `async process(input_data)` - Process input (must override)
- `async initialize()` - Optional initialization
- `async shutdown()` - Optional cleanup

## Development

### Project Structure

```
heimdall/
├── heimdall/
│   ├── __init__.py
│   ├── assistant.py          # Main assistant orchestrator
│   ├── layers/
│   │   ├── __init__.py
│   │   ├── base.py           # Base layer interface
│   │   ├── security.py       # Security/firewall layer
│   │   ├── voice.py          # Voice processing layer
│   │   └── thinking.py       # AI thinking layer
│   └── utils/
│       ├── __init__.py
│       └── config.py         # Configuration utilities
├── examples/
│   ├── basic_usage.py
│   └── custom_layer.py
├── config.yml
├── requirements.txt
├── setup.py
└── README.md
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
