"""
Heimdall - AI Personal Assistant and Firewall
Detects malware and dispatches Gulltoppr for removal
"""

from gulltoppr import Gulltoppr


class Heimdall:
    """
    Heimdall is an AI personal assistant that also serves as a firewall.
    When malware is detected, it dispatches Gulltoppr to handle the threat.
    Named after the Norse god who guards Asgard.
    """
    
    def __init__(self):
        self.gulltoppr = Gulltoppr()
        self.detection_log = []
        self.alerts = []
    
    def scan(self, path):
        """
        Scan a path for malware.
        
        Args:
            path (str): Path to scan for malware
        
        Returns:
            dict: Scan results including any detected threats
        """
        # Simulate malware detection
        # In a real implementation, this would use actual malware detection logic
        scan_result = {
            'path': path,
            'scanned': True,
            'malware_detected': False,
            'threats': []
        }
        
        # Log the scan
        self.detection_log.append(f"Scanned: {path}")
        
        return scan_result
    
    def detect_malware(self, scan_data):
        """
        Analyze scan data to detect malware.
        
        Args:
            scan_data (dict): Data to analyze for malware signatures
                - path: Location being scanned
                - signatures: List of detected signatures
                - behavior: Observed behavior patterns
        
        Returns:
            dict: Detection result with malware information if found
        """
        path = scan_data.get('path', 'unknown')
        signatures = scan_data.get('signatures', [])
        behavior = scan_data.get('behavior', [])
        
        # Check for malware indicators
        malware_detected = False
        malware_info = None
        
        if signatures or behavior:
            # Determine threat level based on signatures and behavior
            threat_level = 'low'
            malware_type = 'unknown'
            
            if any('trojan' in sig.lower() for sig in signatures):
                malware_type = 'trojan'
                threat_level = 'critical'
            elif any('virus' in sig.lower() for sig in signatures):
                malware_type = 'virus'
                threat_level = 'high'
            elif any('spyware' in sig.lower() for sig in signatures):
                malware_type = 'spyware'
                threat_level = 'high'
            elif any('adware' in sig.lower() for sig in signatures):
                malware_type = 'adware'
                threat_level = 'medium'
            elif behavior:
                malware_type = 'suspicious'
                threat_level = 'medium'
            
            if malware_type != 'unknown':
                malware_detected = True
                malware_info = {
                    'path': path,
                    'type': malware_type,
                    'threat_level': threat_level,
                    'signatures': signatures,
                    'behavior': behavior
                }
        
        result = {
            'malware_detected': malware_detected,
            'malware_info': malware_info
        }
        
        if malware_detected:
            self.detection_log.append(f"Malware detected: {malware_type} at {path}")
            self.alerts.append(malware_info)
        
        return result
    
    def dispatch_gulltoppr(self, malware_info):
        """
        Dispatch Gulltoppr to remove detected malware.
        
        Args:
            malware_info (dict): Information about the detected malware
        
        Returns:
            dict: Result of the removal operation
        """
        # Dispatch Gulltoppr to handle the threat
        removal_result = self.gulltoppr.remove_malware(malware_info)
        
        # Log the dispatch
        self.detection_log.append(
            f"Dispatched Gulltoppr for {malware_info.get('type')} at {malware_info.get('path')}"
        )
        
        return removal_result
    
    def process_threat(self, scan_data):
        """
        Complete threat processing pipeline: detect malware and dispatch Gulltoppr if found.
        
        Args:
            scan_data (dict): Data to analyze for malware
        
        Returns:
            dict: Complete processing result
        """
        # Detect malware
        detection_result = self.detect_malware(scan_data)
        
        result = {
            'detection': detection_result,
            'removal': None
        }
        
        # If malware is detected, dispatch Gulltoppr
        if detection_result['malware_detected']:
            malware_info = detection_result['malware_info']
            removal_result = self.dispatch_gulltoppr(malware_info)
            result['removal'] = removal_result
        
        return result
    
    def get_detection_log(self):
        """
        Get the log of all detection and dispatch operations.
        
        Returns:
            list: List of log entries
        """
        return self.detection_log.copy()
    
    def get_alerts(self):
        """
        Get all malware alerts.
        
        Returns:
            list: List of malware alerts
        """
        return self.alerts.copy()
