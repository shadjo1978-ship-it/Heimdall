"""
Heimdall - A.I personal assistant with real-time thinking and voice that serves as a firewall.
"""

__version__ = "0.1.0"

from .malware_detector import WindowsDefenderMalwareDetector

__all__ = ["WindowsDefenderMalwareDetector"]
