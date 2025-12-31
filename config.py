"""
Configuration module for Heimdall malware detection listener
"""

import os
from typing import Dict, Any


class Config:
    """Configuration settings for the malware detection listener"""
    
    # Logging settings
    LOG_LEVEL = os.getenv('HEIMDALL_LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Listener settings
    LISTENER_NAME = os.getenv('HEIMDALL_LISTENER_NAME', 'Heimdall-MalwareListener')
    
    # Detection settings
    ALERT_ON_SEVERITY = os.getenv('HEIMDALL_ALERT_SEVERITY', 'MEDIUM')
    ENABLE_QUARANTINE = os.getenv('HEIMDALL_ENABLE_QUARANTINE', 'false').lower() == 'true'
    QUARANTINE_PATH = os.getenv('HEIMDALL_QUARANTINE_PATH', '/tmp/heimdall/quarantine')
    
    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """Return configuration as a dictionary"""
        return {
            'log_level': cls.LOG_LEVEL,
            'log_format': cls.LOG_FORMAT,
            'listener_name': cls.LISTENER_NAME,
            'alert_on_severity': cls.ALERT_ON_SEVERITY,
            'enable_quarantine': cls.ENABLE_QUARANTINE,
            'quarantine_path': cls.QUARANTINE_PATH
        }
