#!/usr/bin/env python3
"""
Heimdall - Malware Detection Listener
Main entry point for the malware detection listening service
"""

import logging
import signal
import sys
from datetime import datetime

from malware_listener import MalwareDetectionListener, MalwareDetection, DetectionSeverity
from config import Config
from handlers import (
    log_detection_handler,
    alert_critical_handler,
    quarantine_handler,
    statistics_handler
)


def setup_logging():
    """Configure logging for the application"""
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL),
        format=Config.LOG_FORMAT
    )


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    logger = logging.getLogger('heimdall.main')
    logger.info(f"Received signal {signum}, shutting down...")
    sys.exit(0)


def main():
    """Main entry point for the Heimdall malware detection listener"""
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger('heimdall.main')
    
    logger.info("Starting Heimdall Malware Detection Listener")
    logger.info(f"Configuration: {Config.to_dict()}")
    
    # Create listener
    listener = MalwareDetectionListener(name=Config.LISTENER_NAME)
    
    # Register handlers
    listener.register_handler(log_detection_handler)
    listener.register_handler(alert_critical_handler)
    
    if Config.ENABLE_QUARANTINE:
        listener.register_handler(quarantine_handler)
    
    listener.register_handler(statistics_handler)
    
    # Start listener
    listener.start()
    
    # Setup signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    logger.info(f"Listener started with {len(listener.handlers)} handlers")
    logger.info("Press Ctrl+C to stop")
    
    # Demo: Process a sample detection
    logger.info("Processing sample malware detection...")
    sample_detection = MalwareDetection(
        threat_name="Trojan.Generic.Test",
        severity=DetectionSeverity.HIGH,
        file_path="/tmp/suspicious_file.exe",
        metadata={
            "hash": "abc123def456",
            "source": "real-time-scanner"
        }
    )
    
    listener.process_detection(sample_detection)
    
    logger.info("Sample detection processed. Listener is now running...")
    logger.info("Status: " + str(listener.get_status()))
    
    # In a real implementation, this would be an event loop
    # that monitors for actual malware detections
    try:
        while listener.is_running:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received")
    finally:
        listener.stop()
        logger.info("Heimdall Malware Detection Listener stopped")


if __name__ == '__main__':
    main()
