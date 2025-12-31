# Heimdall
A.I personal assistant with real time thinking and voice also serves as a firewall

## Malware Detection Listener

Heimdall includes a malware detection listening system that monitors and processes malware detection events.

### Features

- Event-driven malware detection handling
- Configurable severity levels (LOW, MEDIUM, HIGH, CRITICAL)
- Extensible handler system for custom responses
- Built-in handlers for logging, alerting, and quarantine actions
- Environment-based configuration

### Quick Start

1. Run the malware detection listener:
```bash
python3 main.py
```

2. Configure using environment variables:
```bash
export HEIMDALL_LOG_LEVEL=DEBUG
export HEIMDALL_ENABLE_QUARANTINE=true
export HEIMDALL_ALERT_SEVERITY=MEDIUM
python3 main.py
```

### Configuration Options

- `HEIMDALL_LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `HEIMDALL_LISTENER_NAME`: Name for the listener instance
- `HEIMDALL_ALERT_SEVERITY`: Minimum severity for alerts (LOW, MEDIUM, HIGH, CRITICAL)
- `HEIMDALL_ENABLE_QUARANTINE`: Enable quarantine handler (true/false)
- `HEIMDALL_QUARANTINE_PATH`: Path for quarantined files

### Architecture

- `malware_listener.py`: Core listener and detection event classes
- `handlers.py`: Example detection event handlers
- `config.py`: Configuration management
- `main.py`: Application entry point

### Custom Handlers

You can create custom handlers by defining functions that accept a `MalwareDetection` object:

```python
def my_custom_handler(detection: MalwareDetection) -> None:
    # Your custom logic here
    print(f"Processing: {detection.threat_name}")

listener.register_handler(my_custom_handler)
```
