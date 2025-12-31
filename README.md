# Heimdall 🛡️

A.I personal assistant with real-time thinking and voice that also serves as a firewall

## Overview

Heimdall is an AI guardian assistant inspired by the all-seeing Norse god who guards the Bifrost bridge. This AI persona stands watch at the gateway between you and the digital realm, providing helpful assistance while ensuring your safety and security.

## Features

- **Real-time Thinking**: See how Heimdall processes and reasons through your requests
- **Voice-ready Interaction**: Natural, conversational communication style
- **Firewall Protection**: Automatic security assessment and warnings for potential threats
- **Personal Assistance**: Help with a wide range of tasks and questions
- **Transparent Operation**: Clear visibility into the AI's decision-making process

## Installation

1. Clone the repository:
```bash
git clone https://github.com/shadjo1978-ship-it/Heimdall.git
cd Heimdall
```

2. (Optional) Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Interactive Mode

Run Heimdall in interactive conversation mode:

```bash
python3 heimdall.py
```

This will start an interactive session where you can chat with Heimdall.

### Command Line Mode

Process a single query from the command line:

```bash
python3 heimdall.py "Hello, who are you?"
```

### View Persona Configuration

See the complete Heimdall persona definition:

```bash
python3 heimdall_persona.py
```

## Examples

```bash
# Interactive mode
$ python3 heimdall.py
💬 You: Hello!

⚠️ Heimdall's Thinking
Let me analyze this query...
Understanding the request and formulating a safe, helpful response.

🛡️ Heimdall's Response
Greetings! I am Heimdall, your AI guardian assistant...

# Command line mode  
$ python3 heimdall.py "What are your capabilities?"

🛡️ Heimdall's Response
I'm designed to assist you with vigilance and wisdom. My capabilities include:
  • real-time thinking
  • voice interaction
  • firewall protection
  • personal assistance
```

## The Heimdall Persona

Heimdall embodies several key characteristics:

- **Vigilant**: Always watching for threats and opportunities
- **Wise**: Provides thoughtful, well-reasoned responses  
- **Protective**: Prioritizes user safety and security
- **Helpful**: Eager to assist with tasks and queries
- **Transparent**: Shows thinking process in real-time

## Architecture

The project consists of two main components:

1. **`heimdall_persona.py`**: Core persona configuration and security assessment
2. **`heimdall.py`**: Main application and interaction interface

## Security Features

Heimdall automatically assesses queries for potential security risks:

- **High Risk**: Sensitive data (passwords, credit cards, private keys)
- **Medium Risk**: System operations (downloads, installations, scripts)
- **Low Risk**: Navigation actions (visits, opens, clicks)

When risks are detected, Heimdall provides clear warnings and guidance.

## Future Enhancements

This is a foundational implementation. Potential future enhancements include:

- Integration with LLM APIs (OpenAI, Anthropic, etc.)
- Voice input/output capabilities
- Advanced firewall and security monitoring
- Plugin system for extended capabilities
- Web interface
- Multi-language support

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is open source and available for use and modification.

## About the Name

In Norse mythology, Heimdall is the vigilant guardian of the Bifrost bridge connecting the realms. He possesses extraordinary sight and hearing, can see for hundreds of miles, and requires less sleep than a bird. This makes him the perfect namesake for an AI assistant that watches over users while helping them navigate the digital realm.
