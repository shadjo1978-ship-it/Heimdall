#!/usr/bin/env python3
"""
Example script demonstrating how to use Heimdall's Windows Defender malware detector.
"""

import logging
from heimdall import WindowsDefenderMalwareDetector

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Demonstrate Windows Defender malware detection capabilities."""
    
    print("=" * 70)
    print("Heimdall - Windows Defender Malware Detector Example")
    print("=" * 70)
    print()
    
    # Initialize the malware detector
    detector = WindowsDefenderMalwareDetector()
    
    # Check if Windows Defender is available
    if not detector.is_available:
        print("⚠️  Windows Defender is not available on this system.")
        print("This example requires Windows with Windows Defender installed.")
        print()
        print("Note: On non-Windows systems, the detector will gracefully")
        print("handle the absence of Windows Defender.")
        return
    
    print("✅ Windows Defender is available and ready to use.")
    print()
    
    # Example 1: Update virus signatures
    print("-" * 70)
    print("Example 1: Updating Windows Defender signatures")
    print("-" * 70)
    print("Updating virus definitions...")
    update_result = detector.update_signatures()
    
    if update_result['updated']:
        print("✅ Signatures updated successfully!")
    else:
        print(f"⚠️  Update failed: {update_result.get('error', 'Unknown error')}")
    print()
    
    # Example 2: Scan a specific file
    print("-" * 70)
    print("Example 2: Scanning a specific file")
    print("-" * 70)
    test_file = __file__  # Scan this example script
    print(f"Scanning file: {test_file}")
    
    scan_result = detector.scan_file(test_file)
    
    if scan_result['scanned']:
        if scan_result['threats_found']:
            print(f"⚠️  Threats detected: {scan_result['threat_count']}")
            print(f"Details: {scan_result['details']}")
        else:
            print("✅ No threats found - file is clean!")
    else:
        print(f"❌ Scan failed: {scan_result.get('error', 'Unknown error')}")
    print()
    
    # Example 3: Scan a directory
    print("-" * 70)
    print("Example 3: Scanning a directory")
    print("-" * 70)
    import os
    test_dir = os.path.dirname(__file__)
    print(f"Scanning directory: {test_dir}")
    
    dir_result = detector.scan_directory(test_dir)
    
    if dir_result['scanned']:
        if dir_result['threats_found']:
            print(f"⚠️  Threats detected: {dir_result['threat_count']}")
            print(f"Details: {dir_result['details']}")
        else:
            print("✅ No threats found - directory is clean!")
    else:
        print(f"❌ Scan failed: {dir_result.get('error', 'Unknown error')}")
    print()
    
    # Example 4: Quick system scan
    print("-" * 70)
    print("Example 4: Performing a quick system scan")
    print("-" * 70)
    print("Starting quick scan (this may take a few minutes)...")
    print("Note: In production, you might want to run this asynchronously.")
    
    # Uncomment the following lines to perform an actual quick scan
    # quick_result = detector.quick_scan()
    # 
    # if quick_result['scanned']:
    #     if quick_result['threats_found']:
    #         print(f"⚠️  Threats detected during quick scan")
    #         print(f"Details: {quick_result['details']}")
    #     else:
    #         print("✅ Quick scan complete - no threats found!")
    # else:
    #     print(f"❌ Quick scan failed: {quick_result.get('error', 'Unknown error')}")
    
    print("(Quick scan example commented out to save time)")
    print()
    
    print("=" * 70)
    print("Examples complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
