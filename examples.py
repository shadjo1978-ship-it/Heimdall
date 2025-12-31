#!/usr/bin/env python3
"""
Example usage of Heimdall AI Personal Assistant

This script demonstrates various ways to use Heimdall and Gulltoppr.
"""

from heimdall import Heimdall


def example_basic_usage():
    """Basic usage example."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Protection Scan")
    print("="*60)
    
    # Initialize Heimdall
    heimdall = Heimdall(voice_enabled=True)
    
    # Perform a protection scan
    heimdall.protect()


def example_custom_scan():
    """Custom scan with specific data."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Custom Data Scan")
    print("="*60)
    
    heimdall = Heimdall(voice_enabled=True)
    
    # Define custom files/processes to scan
    files_to_scan = [
        {'name': 'important_document.pdf', 'location': '/home/user/documents'},
        {'name': 'virus_detected.exe', 'location': '/downloads'},
        {'name': 'malware_payload.dll', 'location': '/temp'},
        {'name': 'safe_application.app', 'location': '/applications'},
    ]
    
    # Scan the custom data
    heimdall.think_aloud("Examining specific files with scrutiny.")
    threats = heimdall.scan_for_threats(files_to_scan)
    
    # Dispatch Gulltoppr if threats are found
    if threats:
        heimdall.dispatch_gulltoppr(threats)
    else:
        print("\nHeimdall: No threats in this dataset. Acceptable.")


def example_continuous_monitoring():
    """Simulate continuous monitoring."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Continuous Monitoring (3 Scans)")
    print("="*60)
    
    heimdall = Heimdall(voice_enabled=True)
    
    # Perform multiple scans
    for i in range(3):
        print(f"\n--- Scan #{i+1} ---")
        heimdall.think_aloud(f"Conducting scan iteration {i+1}...")
        heimdall.protect()
    
    # Final status report
    heimdall.status_report()


def example_manual_threat_handling():
    """Manual threat detection and handling."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Manual Threat Handling")
    print("="*60)
    
    heimdall = Heimdall(voice_enabled=True)
    
    # Scan for threats
    system_data = [
        {'name': 'crypto_miner.exe', 'location': '/hidden/folder'},
        {'name': 'keylogger.dll', 'location': '/system'},
    ]
    
    threats = heimdall.scan_for_threats(system_data)
    
    if threats:
        print(f"\n📋 Detected {len(threats)} threat(s):")
        for threat in threats:
            print(f"   - {threat['name']} [{threat['severity']}]")
        
        # Manually dispatch Gulltoppr
        heimdall.think_aloud("Preparing Gulltoppr for deployment...")
        heimdall.dispatch_gulltoppr(threats)


def example_voice_disabled():
    """Example with voice disabled."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Silent Mode (Voice Disabled)")
    print("="*60)
    
    # Initialize Heimdall without voice
    heimdall = Heimdall(voice_enabled=False)
    
    # Run protection
    heimdall.protect()


if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║              HEIMDALL - USAGE EXAMPLES                     ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    # Run all examples
    example_basic_usage()
    example_custom_scan()
    example_continuous_monitoring()
    example_manual_threat_handling()
    example_voice_disabled()
    
    print("\n" + "="*60)
    print("All examples completed. Heimdall's watch never ends.")
    print("="*60 + "\n")
