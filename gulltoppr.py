"""
Gulltoppr - Malware Removal Component
Dispatched by Heimdall to eliminate detected threats
"""


class Gulltoppr:
    """
    Gulltoppr handles malware removal when dispatched by Heimdall.
    Named after Heimdall's horse in Norse mythology.
    """
    
    def __init__(self):
        self.removal_log = []
    
    def remove_malware(self, malware_info):
        """
        Remove the detected malware.
        
        Args:
            malware_info (dict): Information about the detected malware
                - path: Location of the malware
                - type: Type of malware detected
                - threat_level: Severity of the threat
        
        Returns:
            dict: Result of the removal operation
        """
        result = {
            'success': False,
            'malware': malware_info,
            'action': None,
            'message': None
        }
        
        try:
            # Simulate malware removal
            path = malware_info.get('path', 'unknown')
            malware_type = malware_info.get('type', 'unknown')
            threat_level = malware_info.get('threat_level', 'unknown')
            
            # Log the removal attempt
            log_entry = f"Removing {malware_type} malware at {path} (threat level: {threat_level})"
            self.removal_log.append(log_entry)
            
            # Perform removal action based on threat level
            if threat_level == 'critical':
                result['action'] = 'quarantine_and_delete'
                result['message'] = f"Critical threat quarantined and deleted: {path}"
            elif threat_level == 'high':
                result['action'] = 'quarantine'
                result['message'] = f"High threat quarantined: {path}"
            elif threat_level == 'medium':
                result['action'] = 'isolate'
                result['message'] = f"Medium threat isolated: {path}"
            else:
                result['action'] = 'monitor'
                result['message'] = f"Low threat monitored: {path}"
            
            result['success'] = True
            
        except Exception as e:
            result['message'] = f"Error removing malware: {str(e)}"
        
        return result
    
    def get_removal_log(self):
        """
        Get the log of all removal operations.
        
        Returns:
            list: List of removal log entries
        """
        return self.removal_log.copy()
