"""
Tests for Heimdall's integration with Gulltoppr
"""

import unittest
from heimdall import Heimdall
from gulltoppr import Gulltoppr


class TestGulltopprIntegration(unittest.TestCase):
    """Test that Heimdall properly dispatches Gulltoppr when malware is detected"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.heimdall = Heimdall()
    
    def test_heimdall_has_gulltoppr(self):
        """Test that Heimdall has a Gulltoppr instance"""
        self.assertIsInstance(self.heimdall.gulltoppr, Gulltoppr)
    
    def test_dispatch_gulltoppr_on_malware_detection(self):
        """Test that Heimdall dispatches Gulltoppr when malware is detected"""
        # Simulate malware detection
        scan_data = {
            'path': '/tmp/suspicious_file.exe',
            'signatures': ['trojan.generic'],
            'behavior': ['network_exfiltration']
        }
        
        # Process the threat
        result = self.heimdall.process_threat(scan_data)
        
        # Verify malware was detected
        self.assertTrue(result['detection']['malware_detected'])
        self.assertEqual(result['detection']['malware_info']['type'], 'trojan')
        
        # Verify Gulltoppr was dispatched and removed the malware
        self.assertIsNotNone(result['removal'])
        self.assertTrue(result['removal']['success'])
        self.assertEqual(result['removal']['action'], 'quarantine_and_delete')
    
    def test_no_dispatch_without_malware(self):
        """Test that Gulltoppr is not dispatched when no malware is detected"""
        # Simulate clean scan
        scan_data = {
            'path': '/tmp/clean_file.txt',
            'signatures': [],
            'behavior': []
        }
        
        # Process the threat
        result = self.heimdall.process_threat(scan_data)
        
        # Verify no malware was detected
        self.assertFalse(result['detection']['malware_detected'])
        
        # Verify Gulltoppr was not dispatched
        self.assertIsNone(result['removal'])
    
    def test_dispatch_for_virus(self):
        """Test Gulltoppr dispatch for virus detection"""
        scan_data = {
            'path': '/tmp/virus.exe',
            'signatures': ['virus.win32.generic'],
            'behavior': []
        }
        
        result = self.heimdall.process_threat(scan_data)
        
        self.assertTrue(result['detection']['malware_detected'])
        self.assertEqual(result['detection']['malware_info']['type'], 'virus')
        self.assertEqual(result['detection']['malware_info']['threat_level'], 'high')
        self.assertTrue(result['removal']['success'])
        self.assertEqual(result['removal']['action'], 'quarantine')
    
    def test_dispatch_for_spyware(self):
        """Test Gulltoppr dispatch for spyware detection"""
        scan_data = {
            'path': '/tmp/spyware.dll',
            'signatures': ['spyware.keylogger'],
            'behavior': ['keyboard_monitoring']
        }
        
        result = self.heimdall.process_threat(scan_data)
        
        self.assertTrue(result['detection']['malware_detected'])
        self.assertEqual(result['detection']['malware_info']['type'], 'spyware')
        self.assertEqual(result['detection']['malware_info']['threat_level'], 'high')
        self.assertTrue(result['removal']['success'])
        self.assertEqual(result['removal']['action'], 'quarantine')
    
    def test_dispatch_for_adware(self):
        """Test Gulltoppr dispatch for adware detection"""
        scan_data = {
            'path': '/tmp/adware.js',
            'signatures': ['adware.popup'],
            'behavior': []
        }
        
        result = self.heimdall.process_threat(scan_data)
        
        self.assertTrue(result['detection']['malware_detected'])
        self.assertEqual(result['detection']['malware_info']['type'], 'adware')
        self.assertEqual(result['detection']['malware_info']['threat_level'], 'medium')
        self.assertTrue(result['removal']['success'])
        self.assertEqual(result['removal']['action'], 'isolate')
    
    def test_detection_log_includes_dispatch(self):
        """Test that detection log includes Gulltoppr dispatch events"""
        scan_data = {
            'path': '/tmp/malware.exe',
            'signatures': ['trojan.backdoor'],
            'behavior': []
        }
        
        self.heimdall.process_threat(scan_data)
        
        log = self.heimdall.get_detection_log()
        
        # Check that both detection and dispatch are logged
        self.assertTrue(any('Malware detected' in entry for entry in log))
        self.assertTrue(any('Dispatched Gulltoppr' in entry for entry in log))
    
    def test_gulltoppr_removal_log(self):
        """Test that Gulltoppr maintains a removal log"""
        scan_data = {
            'path': '/tmp/threat.bin',
            'signatures': ['virus.polymorphic'],
            'behavior': []
        }
        
        self.heimdall.process_threat(scan_data)
        
        removal_log = self.heimdall.gulltoppr.get_removal_log()
        
        # Verify the removal was logged
        self.assertEqual(len(removal_log), 1)
        self.assertIn('virus', removal_log[0])
        self.assertIn('/tmp/threat.bin', removal_log[0])
    
    def test_multiple_threats_dispatch_gulltoppr_multiple_times(self):
        """Test that multiple threats result in multiple Gulltoppr dispatches"""
        threats = [
            {
                'path': '/tmp/threat1.exe',
                'signatures': ['trojan.generic'],
                'behavior': []
            },
            {
                'path': '/tmp/threat2.dll',
                'signatures': ['virus.boot'],
                'behavior': []
            },
            {
                'path': '/tmp/threat3.js',
                'signatures': ['adware.banner'],
                'behavior': []
            }
        ]
        
        for threat in threats:
            self.heimdall.process_threat(threat)
        
        # Check that Gulltoppr was dispatched for each threat
        removal_log = self.heimdall.gulltoppr.get_removal_log()
        self.assertEqual(len(removal_log), 3)
        
        # Check that all were logged
        detection_log = self.heimdall.get_detection_log()
        dispatch_entries = [entry for entry in detection_log if 'Dispatched Gulltoppr' in entry]
        self.assertEqual(len(dispatch_entries), 3)


class TestGulltoppr(unittest.TestCase):
    """Test Gulltoppr malware removal functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.gulltoppr = Gulltoppr()
    
    def test_remove_critical_threat(self):
        """Test removal of critical threat"""
        malware_info = {
            'path': '/tmp/critical_malware.exe',
            'type': 'trojan',
            'threat_level': 'critical'
        }
        
        result = self.gulltoppr.remove_malware(malware_info)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['action'], 'quarantine_and_delete')
        self.assertIn('Critical threat', result['message'])
    
    def test_remove_high_threat(self):
        """Test removal of high threat"""
        malware_info = {
            'path': '/tmp/high_malware.dll',
            'type': 'virus',
            'threat_level': 'high'
        }
        
        result = self.gulltoppr.remove_malware(malware_info)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['action'], 'quarantine')
        self.assertIn('High threat', result['message'])
    
    def test_remove_medium_threat(self):
        """Test removal of medium threat"""
        malware_info = {
            'path': '/tmp/medium_malware.js',
            'type': 'adware',
            'threat_level': 'medium'
        }
        
        result = self.gulltoppr.remove_malware(malware_info)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['action'], 'isolate')
        self.assertIn('Medium threat', result['message'])
    
    def test_remove_low_threat(self):
        """Test removal of low threat"""
        malware_info = {
            'path': '/tmp/low_malware.txt',
            'type': 'suspicious',
            'threat_level': 'low'
        }
        
        result = self.gulltoppr.remove_malware(malware_info)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['action'], 'monitor')
        self.assertIn('Low threat', result['message'])


class TestHeimdall(unittest.TestCase):
    """Test Heimdall malware detection functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.heimdall = Heimdall()
    
    def test_detect_trojan(self):
        """Test detection of trojan malware"""
        scan_data = {
            'path': '/tmp/trojan.exe',
            'signatures': ['trojan.backdoor'],
            'behavior': []
        }
        
        result = self.heimdall.detect_malware(scan_data)
        
        self.assertTrue(result['malware_detected'])
        self.assertEqual(result['malware_info']['type'], 'trojan')
        self.assertEqual(result['malware_info']['threat_level'], 'critical')
    
    def test_detect_virus(self):
        """Test detection of virus malware"""
        scan_data = {
            'path': '/tmp/virus.exe',
            'signatures': ['virus.boot'],
            'behavior': []
        }
        
        result = self.heimdall.detect_malware(scan_data)
        
        self.assertTrue(result['malware_detected'])
        self.assertEqual(result['malware_info']['type'], 'virus')
        self.assertEqual(result['malware_info']['threat_level'], 'high')
    
    def test_no_detection_clean_file(self):
        """Test that clean files are not flagged"""
        scan_data = {
            'path': '/tmp/clean.txt',
            'signatures': [],
            'behavior': []
        }
        
        result = self.heimdall.detect_malware(scan_data)
        
        self.assertFalse(result['malware_detected'])
        self.assertIsNone(result['malware_info'])


if __name__ == '__main__':
    unittest.main()
