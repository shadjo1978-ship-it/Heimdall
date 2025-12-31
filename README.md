# Heimdall

A.I personal assistant with real time thinking and voice also serves as a firewall

## Windows Platform Build

Heimdall now supports building native Windows executables!

### Quick Start (Windows)

1. **Install Python 3.8+** from https://www.python.org/
2. **Run the build script:**
   ```cmd
   build_windows.bat
   ```
3. **Find your executable** in the `dist` folder

### Features

- 🎯 Standalone Windows executable (no Python installation required for end users)
- 🔊 Voice interaction support
- 🤖 AI-powered assistance
- 🛡️ Built-in firewall capabilities
- 📦 Easy distribution

### Build Options

- **Batch Script:** `build_windows.bat` - Simple one-click build
- **PowerShell:** `build_windows.ps1` - Advanced build with detailed output
- **Manual:** See [BUILD_WINDOWS.md](BUILD_WINDOWS.md) for detailed instructions

### Requirements

- Windows 10 or Windows 11
- Python 3.8 or higher
- Visual C++ Build Tools (for some dependencies)

### Documentation

- [Windows Build Guide](BUILD_WINDOWS.md) - Complete build instructions
- [Contributing](CONTRIBUTING.md) - How to contribute to the project

### Installation

For end users, simply download the `Heimdall.exe` from the releases page and run it. No installation required!

### Development

For developers who want to contribute:

```cmd
# Clone the repository
git clone https://github.com/shadjo1978-ship-it/Heimdall.git
cd Heimdall

# Install in development mode
pip install -e .
pip install -r requirements-dev.txt

# Run directly
python -m heimdall.main
```

## License

MIT
