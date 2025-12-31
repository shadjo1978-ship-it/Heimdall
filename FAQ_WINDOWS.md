# Heimdall Windows Build - Frequently Asked Questions

## General Questions

### Q: Do I need to install Python to run Heimdall?
**A:** No, if you download the pre-built `Heimdall.exe` from the releases page, it's a standalone executable that doesn't require Python. However, you need Python to *build* Heimdall from source.

### Q: What Windows versions are supported?
**A:** Heimdall supports Windows 10 and Windows 11. Older versions may work but are not officially supported.

### Q: Is Heimdall open source?
**A:** Yes, Heimdall is open source and available on GitHub under the MIT license.

## Build Questions

### Q: The build fails with "Python is not recognized". What should I do?
**A:** 
1. Make sure Python is installed from https://www.python.org/
2. During installation, check "Add Python to PATH"
3. If already installed, manually add Python to PATH
4. Restart your command prompt/PowerShell after installation

### Q: I get errors about missing Visual C++ components. What do I need?
**A:** Some Python packages require C++ build tools. Install:
- Visual Studio with C++ workload, OR
- Visual C++ Build Tools from https://visualstudio.microsoft.com/visual-cpp-build-tools/

### Q: The build succeeds but the .exe is huge (50MB+). Is this normal?
**A:** Yes, this is expected. PyInstaller bundles Python and all dependencies into a single executable. The file size typically ranges from 30-100MB depending on features included.

### Q: Can I reduce the executable size?
**A:** Yes, several options:
1. UPX compression (enabled by default)
2. Remove unused optional dependencies
3. Use `--exclude-module` for large libraries you don't need
4. Build a `--onedir` distribution instead of `--onefile` (multiple files but faster startup)

### Q: How long does the build take?
**A:** Typically 2-5 minutes on a modern PC, depending on:
- CPU speed
- Disk speed (SSD is faster)
- Number of dependencies
- Whether packages need to be downloaded

### Q: Can I build for 32-bit Windows?
**A:** Yes, install 32-bit Python and run the build process. The resulting executable will be 32-bit and work on both 32-bit and 64-bit Windows.

## Runtime Questions

### Q: My antivirus flags Heimdall.exe as suspicious. Is it safe?
**A:** This is a known issue with PyInstaller executables. They are sometimes flagged as false positives because:
- PyInstaller bundles Python runtime
- The executable unpacks itself at runtime
- It's not code-signed

**Solutions:**
- Add an exception in your antivirus
- For distribution, consider code signing the executable
- Build from source yourself to verify it's safe

### Q: The executable takes a long time to start. Why?
**A:** PyInstaller executables:
1. Unpack bundled files to a temp directory on first run
2. Load the Python runtime
3. Import all dependencies

This typically takes 2-5 seconds. Subsequent runs are usually faster.

### Q: Can I distribute Heimdall.exe to other users?
**A:** Yes! The `Heimdall.exe` file is standalone and can be distributed freely. Users can run it without installing Python or any dependencies.

### Q: Does Heimdall need internet connection?
**A:** It depends on which features you use:
- Basic functionality: No internet required
- AI features: May require internet for API calls
- Voice features: Local TTS/STT works offline

## Development Questions

### Q: How do I add new features to Heimdall?
**A:** 
1. Edit the Python source files in `src/heimdall/`
2. Test your changes: `python -m heimdall.main`
3. Rebuild: `pyinstaller heimdall.spec --clean`

### Q: Can I customize the application icon?
**A:** Yes, edit `heimdall.spec` and set:
```python
icon='path/to/your/icon.ico'
```

### Q: How do I create a GUI version instead of console?
**A:** Edit `heimdall.spec` and change:
```python
console=False  # Was True
```

### Q: Can I include additional files in the build?
**A:** Yes, edit `heimdall.spec` and add to the `datas` list:
```python
datas=[
    ('config.ini', '.'),
    ('resources/', 'resources'),
],
```

### Q: How do I debug build issues?
**A:** 
1. Run `validate_build.bat` first
2. Check `build/` directory for build logs
3. Try building with `--debug all` flag
4. Use `--log-level DEBUG` for more information
5. Check PyInstaller warnings in the build output

### Q: Can I use a virtual environment?
**A:** Yes, recommended! See BUILD_WINDOWS.md for instructions.

### Q: How do I update PyInstaller?
**A:** Run:
```cmd
pip install --upgrade pyinstaller
```

## Deployment Questions

### Q: How do I create an installer for Heimdall?
**A:** Use tools like:
- NSIS (Nullsoft Scriptable Install System)
- Inno Setup
- WiX Toolset

See BUILD_WINDOWS.md for more details.

### Q: Can I auto-update Heimdall.exe?
**A:** You'll need to implement auto-update logic in your application. Consider using libraries like `pyupdater` or implementing your own update checker.

### Q: Should I code sign the executable?
**A:** For production distribution, yes. Code signing:
- Reduces antivirus false positives
- Builds user trust
- Required for some corporate environments

### Q: How do I distribute to non-technical users?
**A:** 
1. Create an installer (recommended)
2. Or: ZIP the dist folder with a README
3. Include clear instructions
4. Mention system requirements

## Troubleshooting

### Q: The build fails with "ImportError: No module named X"
**A:** Install missing dependencies:
```cmd
pip install -r requirements-windows.txt
```

### Q: I get "Permission Denied" errors during build
**A:** 
1. Close any running instances of Heimdall
2. Run command prompt as Administrator
3. Check antivirus isn't blocking the build
4. Ensure the directory isn't read-only

### Q: The executable crashes immediately
**A:** 
1. Run from command prompt to see error messages
2. Check event viewer for crash logs
3. Rebuild with `--debug all` flag
4. Verify all dependencies are compatible

### Q: How do I report a bug?
**A:** 
1. Check existing GitHub issues
2. Create a new issue with:
   - Windows version
   - Python version
   - Steps to reproduce
   - Error messages
   - Build command used

## Performance

### Q: Can I make Heimdall run faster?
**A:** 
1. Use `--onedir` instead of `--onefile`
2. Lazy-load heavy modules
3. Optimize Python code
4. Use PyPy instead of CPython (advanced)

### Q: Does Heimdall run on ARM Windows?
**A:** It depends on Python support. As of 2025, Python has ARM64 Windows support, so it should work if you build on ARM Windows.

## Additional Resources

- [Python Documentation](https://docs.python.org/)
- [PyInstaller Manual](https://pyinstaller.org/)
- [Windows App Development](https://learn.microsoft.com/en-us/windows/apps/)

---

Still have questions? Check the GitHub Issues page or create a new issue!
