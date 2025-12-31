# Heimdall
A.I personal assistant with real time thinking and voice also serves as a firewall

## Features

- 🤖 **Online AI Support** - Use OpenAI, Anthropic Claude, or other online AI services
- 💬 **Real-time Thinking** - Get intelligent responses powered by state-of-the-art language models
- 🔒 **Firewall Protection** - Built-in content filtering and keyword blocking
- 🎤 **Voice Ready** - Configuration support for voice integration (coming soon)
- 🔌 **Extensible** - Easy to add new AI providers

## Installation

1. Clone the repository:
```bash
git clone https://github.com/shadjo1978-ship-it/Heimdall.git
cd Heimdall
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your AI provider:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

## Configuration

Edit `config.yaml` to configure your AI provider:

```yaml
ai_provider:
  type: 'openai'  # or 'anthropic'
  api_key: 'your-api-key-here'  # or set via OPENAI_API_KEY environment variable
  model: 'gpt-4'
  temperature: 0.7
  max_tokens: 2000
```

### Supported AI Providers

- **OpenAI** - GPT-4, GPT-3.5-turbo, etc.
  - Set `type: 'openai'`
  - Requires `OPENAI_API_KEY` environment variable
  
- **Anthropic** - Claude models
  - Set `type: 'anthropic'`
  - Requires `ANTHROPIC_API_KEY` environment variable

## Usage

### Single Prompt Mode

Ask Heimdall a single question:

```bash
python main.py --prompt "What is the weather like today?"
```

### Interactive Mode

Have a conversation with Heimdall:

```bash
python main.py --interactive
```

Example session:
```
You: Hello Heimdall!
Heimdall: Hello! I'm Heimdall, your AI personal assistant. How can I help you today?

You: What can you do?
Heimdall: I can help you with various tasks including answering questions, providing information, brainstorming ideas, and more. I use online AI services to provide intelligent, real-time responses.

You: exit
Goodbye!
```

### Custom Configuration

Use a custom configuration file:

```bash
python main.py --config custom_config.yaml --interactive
```

## Security Features

Heimdall includes a built-in firewall for content filtering:

- **Keyword Blocking** - Block prompts containing specific keywords
- **Content Filtering** - Filter inappropriate or sensitive content

Configure in `config.yaml`:

```yaml
firewall:
  enabled: true
  content_filter: true
  blocked_keywords: []
```

## Development

### Project Structure

```
Heimdall/
├── heimdall/
│   ├── __init__.py
│   ├── ai_provider.py          # Abstract base class for AI providers
│   ├── openai_provider.py      # OpenAI implementation
│   ├── anthropic_provider.py   # Anthropic implementation
│   ├── provider_factory.py     # Factory for creating providers
│   ├── config.py               # Configuration loader
│   └── heimdall.py             # Main Heimdall class
├── main.py                      # CLI entry point
├── config.yaml                  # Configuration file
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

### Adding a New AI Provider

1. Create a new provider class inheriting from `AIProvider`
2. Implement `generate_response()` and `is_available()` methods
3. Register in `provider_factory.py`

Example:

```python
from heimdall.ai_provider import AIProvider

class MyCustomProvider(AIProvider):
    def generate_response(self, prompt, context=None):
        # Your implementation
        pass
    
    def is_available(self):
        # Check if provider is ready
        return True
```

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
