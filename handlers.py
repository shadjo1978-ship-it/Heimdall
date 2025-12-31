"""
Example handler functions for malware detections
"""

import logging
from malware_listener import MalwareDetection, DetectionSeverity


logger = logging.getLogger('heimdall.handlers')


def log_detection_handler(detection: MalwareDetection) -> None:
    """
    Simple handler that logs the detection details.
    
    Args:
        detection: The malware detection event
    """
    logger.info(f"Detection logged: {detection.threat_name} in {detection.file_path}")


def alert_critical_handler(detection: MalwareDetection) -> None:
    """
    Handler that creates alerts for critical detections.
    
    Args:
        detection: The malware detection event
    """
    if detection.severity == DetectionSeverity.CRITICAL:
        logger.critical(f"CRITICAL THREAT DETECTED: {detection.threat_name} at {detection.file_path}")
        # In a real implementation, this could send notifications, emails, etc.


def quarantine_handler(detection: MalwareDetection) -> None:
    """
    Handler that could quarantine detected files.
    
    Args:
        detection: The malware detection event
    """
    if detection.severity in [DetectionSeverity.HIGH, DetectionSeverity.CRITICAL]:
        logger.warning(f"File {detection.file_path} should be quarantined")
        # In a real implementation, this would move the file to quarantine


def statistics_handler(detection: MalwareDetection) -> None:
    """
    Handler that could track detection statistics.
    
    Args:
        detection: The malware detection event
    """
    logger.debug(f"Recording detection statistics for {detection.threat_name}")
    # In a real implementation, this would update metrics/statistics
