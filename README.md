# Heimdall

A.I personal assistant with real time thinking and voice also serves as a firewall

## Overview

Heimdall is an AI-powered security system that detects malware and automatically dispatches Gulltoppr to eliminate threats. Named after the Norse god who guards Asgard, Heimdall watches over your system. When a threat is detected, Gulltoppr (Heimdall's horse in Norse mythology) is dispatched to handle the malware.

## Features

- **Malware Detection**: Detects various types of malware including trojans, viruses, spyware, and adware
- **Automatic Response**: When malware is detected, Heimdall automatically dispatches Gulltoppr to handle the threat
- **Threat Levels**: Categorizes threats by severity (critical, high, medium, low) and takes appropriate action
- **Comprehensive Logging**: Maintains detailed logs of all detections and removal operations
- **Multiple Removal Strategies**: Different actions based on threat level (quarantine_and_delete, quarantine, isolate, monitor)

## Architecture

### Heimdall
The main security monitor that:
- Scans files and paths for malware
- Analyzes signatures and behavior patterns
- Detects malware and categorizes threats
- Dispatches Gulltoppr when threats are found
- Maintains detection logs and alerts

### Gulltoppr
The malware removal component that:
- Receives malware information from Heimdall
- Executes removal actions based on threat level
- Maintains a log of all removal operations
- Returns results to Heimdall

## Usage

### Basic Example

```python
from heimdall import Heimdall

# Initialize Heimdall
heimdall = Heimdall()

# Scan for malware
scan_data = {
    'path': '/downloads/suspicious_file.exe',
    'signatures': ['trojan.generic'],
    'behavior': ['network_exfiltration']
}

# Process the threat (detect and dispatch Gulltoppr if needed)
result = heimdall.process_threat(scan_data)

if result['detection']['malware_detected']:
    print(f"Malware detected: {result['detection']['malware_info']['type']}")
    print(f"Removal result: {result['removal']['message']}")
```

### Running the Example

```bash
python example.py
```

This will demonstrate Heimdall detecting various types of malware and dispatching Gulltoppr to handle each threat.

## Testing

Run the test suite:

```bash
python -m unittest test_heimdall -v
```

## Threat Levels

- **Critical**: Immediate quarantine and deletion (e.g., trojans)
- **High**: Quarantine for review (e.g., viruses, spyware)
- **Medium**: Isolate from system (e.g., adware)
- **Low**: Monitor activity (e.g., suspicious behavior)

## API Reference

### Heimdall

- `detect_malware(scan_data)`: Analyze data for malware signatures
- `dispatch_gulltoppr(malware_info)`: Dispatch Gulltoppr to remove malware
- `process_threat(scan_data)`: Complete pipeline: detect and dispatch if needed
- `get_detection_log()`: Get log of all detection and dispatch operations
- `get_alerts()`: Get all malware alerts

### Gulltoppr

- `remove_malware(malware_info)`: Remove detected malware
- `get_removal_log()`: Get log of all removal operations

## License

MIT
