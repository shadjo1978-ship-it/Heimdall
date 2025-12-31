# Heimdall Windows - Quick Start Guide

Get Heimdall up and running on Windows in 5 minutes!

## For End Users (Just Want to Run It)

### Option 1: Download Pre-built Executable (Easiest)
1. Go to [Releases](../../releases)
2. Download `Heimdall.exe`
3. Double-click to run!

No installation needed. No Python required.

### Option 2: Run from Command Line
```cmd
# Download Heimdall.exe to any folder
cd path\to\folder
Heimdall.exe --help
```

That's it! You're done. 🎉

---

## For Developers (Want to Build from Source)

### Prerequisites
- Windows 10 or 11
- 10 minutes
- Internet connection

### Step 1: Install Python (5 minutes)
1. Download from https://www.python.org/ (get Python 3.11 or newer)
2. Run installer
3. ⚠️ **IMPORTANT:** Check "Add Python to PATH"
4. Click "Install Now"
5. Close installer when done

### Step 2: Get Heimdall (1 minute)
```cmd
# Option A: Download ZIP
# Go to https://github.com/shadjo1978-ship-it/Heimdall
# Click "Code" → "Download ZIP"
# Extract to a folder

# Option B: Use Git (if installed)
git clone https://github.com/shadjo1978-ship-it/Heimdall.git
cd Heimdall
```

### Step 3: Build (2 minutes)
```cmd
# Navigate to Heimdall folder
cd path\to\Heimdall

# Run build script
build_windows.bat
```

The script will:
1. Install build tools
2. Install dependencies
3. Build Heimdall.exe

### Step 4: Run (10 seconds)
```cmd
cd dist
Heimdall.exe
```

You're done! 🚀

---

## Common Issues

### "Python is not recognized"
**Solution:** Python is not in PATH. Reinstall Python and check "Add Python to PATH"

### Build fails
**Solution:** Run `validate_build.bat` to diagnose the issue

### Antivirus blocks Heimdall.exe
**Solution:** This is a false positive. Add an exception for Heimdall.exe

---

## What's Next?

### Customize Heimdall
- Edit `src/heimdall/` files
- Add AI features
- Add voice features
- Add firewall rules

### Create an Installer
See [BUILD_WINDOWS.md](BUILD_WINDOWS.md) for NSIS/Inno Setup instructions

### Distribute to Others
1. Build Heimdall.exe
2. ZIP the `dist` folder
3. Share with anyone - no Python needed!

---

## Need Help?

- 📖 Read [BUILD_WINDOWS.md](BUILD_WINDOWS.md) for detailed instructions
- ❓ Check [FAQ_WINDOWS.md](FAQ_WINDOWS.md) for common questions
- 🐛 Report issues on [GitHub](../../issues)

Happy building! 🔨
