# Building Heimdall for Windows

This guide explains how to build Heimdall AI Personal Assistant for the Windows platform.

## Prerequisites

### Required Software

1. **Python 3.8 or higher**
   - Download from: https://www.python.org/downloads/
   - During installation, make sure to check "Add Python to PATH"
   - Verify installation: `python --version`

2. **Git** (optional, for cloning the repository)
   - Download from: https://git-scm.com/download/win
   - Verify installation: `git --version`

3. **Visual C++ Build Tools** (required for some Python packages)
   - Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - Or install Visual Studio with C++ development workload

## Quick Start

### Option 1: Using Batch Script (Recommended for beginners)

1. Open Command Prompt in the Heimdall directory
2. Run the build script:
   ```cmd
   build_windows.bat
   ```

### Option 2: Using PowerShell Script

1. Open PowerShell in the Heimdall directory
2. You may need to allow script execution:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
3. Run the build script:
   ```powershell
   .\build_windows.ps1
   ```

### Option 3: Manual Build Steps

1. **Install dependencies:**
   ```cmd
   python -m pip install --upgrade pip
   python -m pip install -r requirements-windows.txt
   ```

2. **Install Heimdall in development mode:**
   ```cmd
   python -m pip install -e .
   ```

3. **Build the executable:**
   ```cmd
   pyinstaller heimdall.spec --clean --noconfirm
   ```

4. **Find the executable:**
   - The built executable will be in the `dist` directory
   - File: `dist\Heimdall.exe`

## Running Heimdall

After building, you can run Heimdall in two ways:

### From the dist directory:
```cmd
cd dist
Heimdall.exe
```

### With command-line options:
```cmd
Heimdall.exe --help
Heimdall.exe --verbose
Heimdall.exe --version
```

## Build Output

The build process creates the following directories:

- `build/` - Intermediate build files (can be deleted)
- `dist/` - Final executable and dependencies
  - `Heimdall.exe` - The standalone Windows executable

## Distribution

The `Heimdall.exe` file in the `dist` directory is a standalone executable that includes all necessary dependencies. You can:

1. Copy `dist\Heimdall.exe` to any Windows PC
2. Run it without installing Python or other dependencies
3. Share it with other users

## Customization

### Change Application Icon

1. Create or obtain a `.ico` file
2. Place it in the project root (e.g., `heimdall.ico`)
3. Edit `heimdall.spec` and update the icon parameter:
   ```python
   icon='heimdall.ico',
   ```

### Build GUI Version (No Console Window)

Edit `heimdall.spec` and change:
```python
console=True,  # Change to False
```

### Include Additional Files

Edit `heimdall.spec` and add files to the `datas` list:
```python
datas=[
    ('README.md', '.'),
    ('config.ini', '.'),  # Add your files here
],
```

## Creating an Installer

### Using NSIS (Nullsoft Scriptable Install System)

1. Download and install NSIS: https://nsis.sourceforge.io/
2. Create an installer script (example provided in `installer.nsi` if available)
3. Compile the installer with NSIS

### Using Inno Setup

1. Download and install Inno Setup: https://jrsoftware.org/isinfo.php
2. Create a setup script
3. Compile to create an installer

## Troubleshooting

### "Python is not recognized"
- Make sure Python is installed and added to PATH
- Restart Command Prompt/PowerShell after installation
- Try `py --version` instead of `python --version`

### "pyinstaller: command not found"
- Install PyInstaller: `pip install pyinstaller`
- Make sure pip's Scripts directory is in PATH

### Missing DLLs or Dependencies
- Make sure Visual C++ Redistributable is installed
- Some packages may require additional system libraries

### Build Fails with Import Errors
- Check that all required packages are installed
- Try installing in a fresh virtual environment

### Antivirus False Positives
- PyInstaller executables are sometimes flagged by antivirus software
- This is a known issue with PyInstaller
- You may need to add an exception or use code signing

## Advanced Configuration

### Virtual Environment (Recommended)

Use a virtual environment for clean builds:

```cmd
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements-windows.txt

# Build
pyinstaller heimdall.spec --clean
```

### Code Signing

For production releases, consider code signing your executable:

1. Obtain a code signing certificate
2. Use `signtool.exe` from Windows SDK
3. Update `heimdall.spec` with signing parameters

## Performance Optimization

### Reduce Executable Size

1. Use UPX compression (enabled by default in `heimdall.spec`)
2. Exclude unnecessary modules in `heimdall.spec`
3. Use `--onefile` for a single executable (slower startup)

### Faster Startup

- Use `--onedir` instead of `--onefile` (default in `heimdall.spec`)
- Minimize hidden imports
- Lazy-load heavy modules

## Additional Resources

- PyInstaller Documentation: https://pyinstaller.org/
- Python Packaging Guide: https://packaging.python.org/
- Windows App Certification Kit: https://learn.microsoft.com/en-us/windows/apps/

## Support

For build issues or questions:
1. Check the GitHub Issues page
2. Review PyInstaller documentation
3. Ensure all prerequisites are properly installed
