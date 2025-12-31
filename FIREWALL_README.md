# Heimdall Firewall Engine

## Overview

Heimdall is an AI personal assistant with real-time thinking and voice capabilities that also serves as a firewall. This firewall engine provides comprehensive packet filtering and network security features.

## Features

- **Rule-based packet filtering**: Define custom rules with protocol, IP address, and port matching
- **IP blacklisting and whitelisting**: Quick blocking or allowing of specific IP addresses
- **Port-based filtering**: Block or allow specific ports
- **Priority-based rule evaluation**: Control the order of rule processing
- **Comprehensive logging**: Track all packet decisions with detailed logs
- **Statistics tracking**: Monitor firewall activity and performance
- **Configuration management**: Save and load firewall configurations in JSON or YAML format
- **CLI interface**: Easy-to-use command-line interface for firewall management

## Installation

1. Install Python 3.7 or higher
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### Using the Python API

```python
from firewall_engine import FirewallEngine, FirewallRule, Action, Protocol

# Create a firewall instance
firewall = FirewallEngine(default_action=Action.DENY)

# Add a rule to allow HTTP traffic
rule = FirewallRule(
    name="allow_http",
    action=Action.ALLOW,
    protocol=Protocol.TCP,
    dest_port=80
)
firewall.add_rule(rule)

# Add an IP to the blacklist
firewall.add_to_blacklist("192.168.1.100")

# Test a packet
packet = {
    'protocol': 'tcp',
    'source_ip': '10.0.0.1',
    'dest_ip': '8.8.8.8',
    'dest_port': 80
}
action, reason = firewall.process_packet(packet)
print(f"Packet {action.value}: {reason}")
```

### Using the CLI

```bash
# Make the CLI executable
chmod +x firewall_cli.py

# Add a firewall rule
./firewall_cli.py add-rule allow_ssh allow --protocol tcp --dest-port 22

# Add an IP to the blacklist
./firewall_cli.py blacklist 192.168.1.100

# Test a packet
./firewall_cli.py test-packet --protocol tcp --source-ip 10.0.0.1 --dest-ip 8.8.8.8 --dest-port 80

# View firewall status
./firewall_cli.py status

# Load configuration from file
./firewall_cli.py load-config example_config.json --format json

# Save configuration to file
./firewall_cli.py save-config my_config.json --format json
```

## Configuration

### Configuration File Format

Configuration files can be in JSON or YAML format. Here's an example:

```json
{
  "default_action": "deny",
  "rules": [
    {
      "name": "allow_http",
      "action": "allow",
      "protocol": "tcp",
      "dest_port": 80,
      "priority": 10,
      "enabled": true
    }
  ],
  "blacklist": ["10.0.0.1"],
  "whitelist": ["8.8.8.8"],
  "blocked_ports": [23, 21],
  "allowed_ports": []
}
```

## Firewall Rules

Rules support the following parameters:

- **name**: Unique identifier for the rule
- **action**: "allow" or "deny"
- **protocol**: "tcp", "udp", "icmp", or "any"
- **source_ip**: Source IP address or CIDR range (optional)
- **dest_ip**: Destination IP address or CIDR range (optional)
- **source_port**: Source port number (optional)
- **dest_port**: Destination port number (optional)
- **priority**: Rule priority (lower number = higher priority, default: 100)
- **enabled**: Whether the rule is active (default: true)

## Rule Evaluation Order

The firewall evaluates packets in the following order:

1. **Firewall enabled check**: If disabled, all packets are allowed
2. **Whitelist**: IPs in the whitelist are immediately allowed
3. **Blacklist**: IPs in the blacklist are immediately denied
4. **Blocked ports**: Packets to blocked ports are denied
5. **Allowed ports**: If allowed ports are configured, only those ports are permitted
6. **Rules**: Rules are evaluated in priority order (lower priority number first)
7. **Default action**: If no rules match, the default action is applied

## CLI Commands

### Rule Management
- `add-rule <name> <action>`: Add a firewall rule
- `remove-rule <name>`: Remove a firewall rule
- `enable-rule <name>`: Enable a rule
- `disable-rule <name>`: Disable a rule
- `list-rules`: List all rules

### IP Management
- `blacklist <ip>`: Add IP to blacklist
- `unblacklist <ip>`: Remove IP from blacklist
- `whitelist <ip>`: Add IP to whitelist
- `unwhitelist <ip>`: Remove IP from whitelist

### Port Management
- `block-port <port>`: Block a port
- `unblock-port <port>`: Unblock a port
- `allow-port <port>`: Add port to allowlist

### Testing
- `test-packet`: Test a packet against firewall rules

### Information
- `status`: Show firewall status
- `stats`: Show firewall statistics
- `logs [--limit N]`: Show packet logs

### Configuration
- `load-config <filepath>`: Load configuration from file
- `save-config <filepath>`: Save configuration to file

### Control
- `enable`: Enable the firewall
- `disable`: Disable the firewall

## Testing

Run the test suite:

```bash
python -m pytest test_firewall.py -v
```

Or using unittest:

```bash
python -m unittest test_firewall.py
```

## Examples

### Example 1: Basic Web Server Protection

```python
from firewall_engine import FirewallEngine, FirewallRule, Action, Protocol

firewall = FirewallEngine(default_action=Action.DENY)

# Allow HTTP and HTTPS
firewall.add_rule(FirewallRule(
    name="allow_http",
    action=Action.ALLOW,
    protocol=Protocol.TCP,
    dest_port=80,
    priority=10
))

firewall.add_rule(FirewallRule(
    name="allow_https",
    action=Action.ALLOW,
    protocol=Protocol.TCP,
    dest_port=443,
    priority=10
))

# Block specific malicious IP
firewall.add_to_blacklist("192.168.1.100")
```

### Example 2: Internal Network Protection

```python
from firewall_engine import FirewallEngine, FirewallRule, Action, Protocol

firewall = FirewallEngine(default_action=Action.ALLOW)

# Block external access to internal network
firewall.add_rule(FirewallRule(
    name="block_external_to_internal",
    action=Action.DENY,
    dest_ip="192.168.0.0/16",
    priority=1
))

# Block dangerous ports
firewall.block_port(23)  # Telnet
firewall.block_port(21)  # FTP
firewall.block_port(445) # SMB
```

### Example 3: Using Configuration Files

```python
from firewall_engine import FirewallEngine, Action
from firewall_config import FirewallConfig

firewall = FirewallEngine(default_action=Action.DENY)

# Load configuration
FirewallConfig.load_from_json("example_config.json", firewall)

# Process packets
packet = {
    'protocol': 'tcp',
    'source_ip': '10.0.0.1',
    'dest_ip': '8.8.8.8',
    'dest_port': 80
}
action, reason = firewall.process_packet(packet)

# Save updated configuration
FirewallConfig.save_to_json("updated_config.json", firewall)
```

## Architecture

The firewall engine consists of three main components:

1. **firewall_engine.py**: Core firewall logic with packet filtering
2. **firewall_config.py**: Configuration management (JSON/YAML support)
3. **firewall_cli.py**: Command-line interface

## Security Considerations

- Default deny policy is recommended for maximum security
- Whitelist has the highest priority to ensure critical services remain accessible
- Rules are evaluated in priority order for predictable behavior
- All packet decisions are logged for audit purposes
- Input validation is performed on all IP addresses and port numbers

## License

This project is part of the Heimdall AI personal assistant.

## Contributing

Contributions are welcome! Please ensure all tests pass before submitting changes.
