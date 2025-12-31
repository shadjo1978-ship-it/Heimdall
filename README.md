# Heimdall
A.I personal assistant with real time thinking and voice also serves as a firewall

## Firewall Engine

Heimdall includes a comprehensive firewall engine for network security and packet filtering.

### Features

- **Rule-based packet filtering** with protocol, IP, and port matching
- **IP blacklisting and whitelisting** for quick access control
- **Port-based filtering** to block or allow specific ports
- **Priority-based rule evaluation** for predictable behavior
- **Comprehensive logging** and statistics tracking
- **Configuration management** with JSON/YAML support
- **Command-line interface** for easy management

### Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the demo
python demo.py

# Use the CLI
python firewall_cli.py --help

# Test a packet
python firewall_cli.py test-packet --protocol tcp --source-ip 10.0.0.1 --dest-ip 8.8.8.8 --dest-port 80
```

### Documentation

See [FIREWALL_README.md](FIREWALL_README.md) for complete documentation, examples, and API reference.
