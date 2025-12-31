# Heimdall

A.I personal assistant with real-time thinking and voice that also serves as a firewall with integrated malware detection.

## Features

- **Windows Defender Integration**: Uses Windows Defender as the primary malware detection engine
- **File Scanning**: Scan individual files for malware threats
- **Directory Scanning**: Recursively scan directories for threats
- **Quick System Scan**: Perform quick scans of common system areas
- **Signature Updates**: Keep malware definitions up-to-date
- **Cross-platform Support**: Gracefully handles non-Windows environments

## Installation

1. Clone the repository:
```bash
git clone https://github.com/shadjo1978-ship-it/Heimdall.git
cd Heimdall
```

2. Install dependencies (optional):
```bash
pip install -r requirements.txt
```

## Requirements

- **Windows OS**: Windows Defender malware detection requires Windows 10 or later
- **Python 3.7+**: The application is written in Python
- **Administrator Privileges**: Some Windows Defender operations may require elevated permissions

## Usage

### Basic Example

```python
from heimdall import WindowsDefenderMalwareDetector

# Initialize the malware detector
detector = WindowsDefenderMalwareDetector()

# Check if Windows Defender is available
if detector.is_available:
    # Scan a file
    result = detector.scan_file("path/to/file.exe")
    
    if result['scanned'] and not result['threats_found']:
        print("File is clean!")
    elif result['threats_found']:
        print(f"Threats detected: {result['threat_count']}")
    else:
        print(f"Scan error: {result['error']}")
```

### Running the Example

See the example script for more detailed usage:

```bash
cd examples
python defender_example.py
```

### Available Methods

#### `scan_file(file_path: str) -> Dict`
Scan a single file for malware.

**Parameters:**
- `file_path`: Path to the file to scan

**Returns:**
- Dictionary with scan results including `scanned`, `threats_found`, `threat_count`, `details`, and `error`

#### `scan_directory(directory_path: str) -> Dict`
Scan a directory for malware.

**Parameters:**
- `directory_path`: Path to the directory to scan

**Returns:**
- Dictionary with scan results

#### `quick_scan() -> Dict`
Perform a quick scan of common system areas.

**Returns:**
- Dictionary with scan results

#### `update_signatures() -> Dict`
Update Windows Defender virus definitions.

**Returns:**
- Dictionary with update results including `updated`, `details`, and `error`

## Configuration

Edit `config.env` to customize settings:

- `DEFENDER_PATH`: Path to Windows Defender executable (default: `C:\Program Files\Windows Defender\MpCmdRun.exe`)
- `FILE_SCAN_TIMEOUT`: Timeout for file scans in seconds (default: 300)
- `DIRECTORY_SCAN_TIMEOUT`: Timeout for directory scans in seconds (default: 600)
- `QUICK_SCAN_TIMEOUT`: Timeout for quick scans in seconds (default: 600)
- `LOG_LEVEL`: Logging level (default: INFO)

## Windows Defender Command-Line Tool

This implementation uses Windows Defender's command-line tool (`MpCmdRun.exe`) which provides:

- **Scan Types**:
  - Type 1: Quick scan
  - Type 2: Full scan
  - Type 3: Custom scan (file or directory)
  
- **Operations**:
  - `-Scan`: Perform malware scans
  - `-SignatureUpdate`: Update virus definitions
  - `-?`: Display help information

## Security Notes

- Always keep Windows Defender signatures up-to-date
- Run scans with appropriate permissions
- Review scan results and take appropriate action on threats
- Consider scheduling regular scans for proactive protection

## Limitations

- Requires Windows operating system with Windows Defender installed
- Some operations require administrator privileges
- Scan performance depends on file size and system resources
- On non-Windows systems, the detector will report that Windows Defender is unavailable

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or contributions, please open an issue on GitHub.
