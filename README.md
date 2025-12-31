# Heimdall

**AI Personal Assistant with Real-Time Thinking, Voice, and Firewall Capabilities**

> "I see all. I protect all." - Heimdall

## Overview

Heimdall is an AI personal assistant that combines real-time thinking capabilities with voice output and advanced firewall protection. When Heimdall detects a virus or threat, it dispatches **Gulltoppr** (named after Heimdall's golden-maned horse from Norse mythology) to eliminate it.

### Personality

Heimdall embodies a unique personality blend:
- **Heimdall from God of War**: Vigilant, all-seeing, and protective
- **Tywin Lannister**: Strategic, commanding, direct, and no-nonsense

This creates an AI that is both watchful and stern, protective yet uncompromising.

## Features

✨ **Real-Time Thinking**: Heimdall streams its thought process, allowing you to see its decision-making in real-time

🔊 **Voice Output**: Text-to-speech capability (simulated by default, can be enhanced with pyttsx3)

🛡️ **Firewall Protection**: Continuously scans for threats and security vulnerabilities

⚔️ **Gulltoppr Dispatch**: Automatically eliminates detected viruses and threats

📊 **Status Reporting**: Provides detailed reports on scans, threats, and eliminations

## Installation

### Basic Installation

No external dependencies required! Heimdall uses Python's standard library.

```bash
# Clone the repository
git clone https://github.com/shadjo1978-ship-it/Heimdall.git
cd Heimdall

# Run Heimdall
python3 heimdall.py
```

### Enhanced Installation (Optional)

For real text-to-speech and system monitoring:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from heimdall import Heimdall

# Initialize Heimdall
heimdall = Heimdall(voice_enabled=True)

# Perform a protection scan
heimdall.protect()

# Get status report
heimdall.status_report()
```

### Running the Demo

```bash
python3 heimdall.py
```

This will run a demonstration showing:
1. Heimdall's initialization and greeting
2. Real-time thinking process
3. System scanning for threats
4. Gulltoppr dispatch to eliminate detected threats
5. Status reporting
6. Custom scan demonstration

### Advanced Usage

```python
from heimdall import Heimdall

# Initialize Heimdall
heimdall = Heimdall(voice_enabled=True)

# Custom data scan
custom_data = [
    {'name': 'suspicious_file.exe', 'location': '/downloads'},
    {'name': 'document.pdf', 'location': '/documents'},
]

# Scan custom data
threats = heimdall.scan_for_threats(custom_data)

# Dispatch Gulltoppr if threats found
if threats:
    heimdall.dispatch_gulltoppr(threats)
```

## Architecture

### Core Components

1. **Heimdall Class**: Main AI assistant
   - Real-time thinking
   - Threat scanning
   - Voice output
   - Command and control

2. **Gulltoppr Class**: Threat elimination system
   - Receives threats from Heimdall
   - Eliminates detected viruses
   - Tracks elimination history

### Personality System

Heimdall's personality is implemented through:
- **Response Templates**: Pre-defined phrases matching character traits
- **Thinking Patterns**: Strategic and observant thought processes
- **Voice Tone**: Direct, commanding, and vigilant

## Example Output

```
╔════════════════════════════════════════════════════════════╗
║                        HEIMDALL                            ║
║          AI Personal Assistant & Firewall System           ║
║                                                            ║
║  "I see all. I protect all."                              ║
╚════════════════════════════════════════════════════════════╝

============================================================
HEIMDALL - AI PERSONAL ASSISTANT & FIREWALL
============================================================

🔊 Heimdall: I see all. What requires my attention?

💭 Heimdall's thoughts: I observe...
   The realms require constant vigilance.

------------------------------------------------------------
INITIATING SYSTEM SCAN
------------------------------------------------------------

💭 Heimdall's thoughts: Scanning all realms for threats...
   Scanning all realms for threats...

⚠️  1 threat(s) detected!
  1. suspicious_virus.exe [CRITICAL] @ /temp/downloads

🔊 Heimdall: Foolish. Did they think I wouldn't see this?

⚔️  Gulltoppr dispatched to eliminate: suspicious_virus.exe
    Threat level: CRITICAL
    Location: /temp/downloads
    ✓ Threat neutralized

🔊 Heimdall: The threat has been dealt with. As expected.
```

## Customization

### Adjusting Personality

Edit the response templates in `heimdall.py`:

```python
GREETINGS = [
    "I see all. What requires my attention?",
    # Add your custom greetings
]

VIRUS_DETECTED_RESPONSES = [
    "A threat approaches. How predictable.",
    # Add your custom responses
]
```

### Enhancing Threat Detection

Modify the `_analyze_threat_level` method to implement custom threat detection logic:

```python
def _analyze_threat_level(self, item: Dict) -> int:
    # Add your custom threat detection logic
    pass
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Credits

- Inspired by **Heimdall** from Norse mythology and God of War
- Character traits influenced by **Tywin Lannister** from Game of Thrones
- **Gulltoppr**: Named after Heimdall's horse in Norse mythology
