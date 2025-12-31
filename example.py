#!/usr/bin/env python
"""
Example demonstration of Heimdall dispatching Gulltoppr when malware is detected
"""

from heimdall import Heimdall


def main():
    print("=" * 60)
    print("Heimdall - AI Personal Assistant and Firewall")
    print("=" * 60)
    print()
    
    # Initialize Heimdall
    heimdall = Heimdall()
    print("✓ Heimdall initialized")
    print("✓ Gulltoppr ready for dispatch")
    print()
    
    # Example 1: Detect and remove a critical trojan
    print("-" * 60)
    print("Example 1: Critical Trojan Detection")
    print("-" * 60)
    
    scan_data_1 = {
        'path': '/downloads/suspicious_installer.exe',
        'signatures': ['trojan.generic', 'trojan.downloader'],
        'behavior': ['network_exfiltration', 'registry_modification']
    }
    
    print(f"Scanning: {scan_data_1['path']}")
    result_1 = heimdall.process_threat(scan_data_1)
    
    if result_1['detection']['malware_detected']:
        malware = result_1['detection']['malware_info']
        print(f"⚠ MALWARE DETECTED!")
        print(f"  Type: {malware['type']}")
        print(f"  Threat Level: {malware['threat_level']}")
        print(f"  Signatures: {', '.join(malware['signatures'])}")
        print()
        print("→ Dispatching Gulltoppr...")
        removal = result_1['removal']
        print(f"✓ {removal['message']}")
        print(f"  Action taken: {removal['action']}")
    print()
    
    # Example 2: Detect and remove a virus
    print("-" * 60)
    print("Example 2: Virus Detection")
    print("-" * 60)
    
    scan_data_2 = {
        'path': '/tmp/infected_document.doc',
        'signatures': ['virus.macro.generic'],
        'behavior': ['file_modification']
    }
    
    print(f"Scanning: {scan_data_2['path']}")
    result_2 = heimdall.process_threat(scan_data_2)
    
    if result_2['detection']['malware_detected']:
        malware = result_2['detection']['malware_info']
        print(f"⚠ MALWARE DETECTED!")
        print(f"  Type: {malware['type']}")
        print(f"  Threat Level: {malware['threat_level']}")
        print()
        print("→ Dispatching Gulltoppr...")
        removal = result_2['removal']
        print(f"✓ {removal['message']}")
        print(f"  Action taken: {removal['action']}")
    print()
    
    # Example 3: Scan a clean file
    print("-" * 60)
    print("Example 3: Clean File Scan")
    print("-" * 60)
    
    scan_data_3 = {
        'path': '/documents/report.pdf',
        'signatures': [],
        'behavior': []
    }
    
    print(f"Scanning: {scan_data_3['path']}")
    result_3 = heimdall.process_threat(scan_data_3)
    
    if not result_3['detection']['malware_detected']:
        print("✓ No malware detected - file is clean")
    print()
    
    # Example 4: Detect and handle adware
    print("-" * 60)
    print("Example 4: Adware Detection")
    print("-" * 60)
    
    scan_data_4 = {
        'path': '/browser/extension.js',
        'signatures': ['adware.popup', 'adware.injector'],
        'behavior': ['browser_injection']
    }
    
    print(f"Scanning: {scan_data_4['path']}")
    result_4 = heimdall.process_threat(scan_data_4)
    
    if result_4['detection']['malware_detected']:
        malware = result_4['detection']['malware_info']
        print(f"⚠ MALWARE DETECTED!")
        print(f"  Type: {malware['type']}")
        print(f"  Threat Level: {malware['threat_level']}")
        print()
        print("→ Dispatching Gulltoppr...")
        removal = result_4['removal']
        print(f"✓ {removal['message']}")
        print(f"  Action taken: {removal['action']}")
    print()
    
    # Show summary
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    
    detection_log = heimdall.get_detection_log()
    removal_log = heimdall.gulltoppr.get_removal_log()
    alerts = heimdall.get_alerts()
    
    print(f"Total scans: {len([e for e in detection_log if 'Malware detected' in e]) + 1}")  # +1 for clean file
    print(f"Malware detected: {len(alerts)}")
    print(f"Gulltoppr dispatches: {len(removal_log)}")
    print()
    
    print("Detection Log:")
    for entry in detection_log:
        print(f"  • {entry}")
    print()
    
    print("Removal Log:")
    for entry in removal_log:
        print(f"  • {entry}")
    print()


if __name__ == '__main__':
    main()
