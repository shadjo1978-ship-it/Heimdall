#!/usr/bin/env python3
"""
Heimdall - AI Personal Assistant with Firewall Capabilities

An AI personal assistant with real-time thinking and voice capabilities
that also serves as a firewall. When Heimdall detects a virus, it dispatches
Gulltoppr to eliminate it.

Personality: Mix of Heimdall from God of War and Tywin Lannister
"""

import time
import random
from typing import List, Dict, Optional
from datetime import datetime


class Gulltoppr:
    """
    Gulltoppr - The virus elimination system dispatched by Heimdall.
    Named after Heimdall's golden-maned horse in Norse mythology.
    """
    
    def __init__(self):
        self.eliminated_threats = []
    
    def eliminate_threat(self, threat: Dict) -> bool:
        """
        Eliminate a detected threat.
        
        Args:
            threat: Dictionary containing threat information
            
        Returns:
            bool: True if threat was eliminated successfully
        """
        print(f"\n⚔️  Gulltoppr dispatched to eliminate: {threat['name']}")
        print(f"    Threat level: {threat['severity']}")
        print(f"    Location: {threat['location']}")
        
        # Simulate elimination process
        time.sleep(0.5)
        
        self.eliminated_threats.append({
            'threat': threat,
            'timestamp': datetime.now().isoformat(),
            'status': 'eliminated'
        })
        
        print(f"    ✓ Threat neutralized")
        return True


class Heimdall:
    """
    Heimdall - AI Personal Assistant with Firewall Capabilities
    
    Personality traits:
    - Vigilant and all-seeing (Heimdall from God of War)
    - Strategic and commanding (Tywin Lannister)
    - Direct and no-nonsense
    - Protective but stern
    """
    
    # Personality-driven response templates
    GREETINGS = [
        "I see all. What requires my attention?",
        "Speak. I have been watching.",
        "Your presence is noted. State your purpose.",
    ]
    
    VIRUS_DETECTED_RESPONSES = [
        "A threat approaches. How predictable.",
        "Foolish. Did they think I wouldn't see this?",
        "Another pest to be dealt with. Tiresome.",
        "Incompetence. This threat will be eliminated.",
    ]
    
    THREAT_ELIMINATED_RESPONSES = [
        "The threat has been dealt with. As expected.",
        "Order is restored. Vigilance continues.",
        "Neutralized. I see everything, and I protect everything.",
        "A minor inconvenience. Nothing escapes my sight.",
    ]
    
    THINKING_PHRASES = [
        "I observe...",
        "Analyzing the situation...",
        "My sight extends beyond mortal perception...",
        "Considering all possibilities...",
        "I see patterns forming...",
    ]
    
    # Threat detection configuration
    SUSPICIOUS_KEYWORDS = ['virus', 'malware', 'trojan', 'backdoor', 'exploit']
    RANDOM_THREAT_PROBABILITY = 0.1  # 10% chance of detecting low-level threat
    
    def __init__(self, voice_enabled: bool = True):
        """
        Initialize Heimdall.
        
        Args:
            voice_enabled: Enable voice output (text-to-speech simulation)
        """
        self.voice_enabled = voice_enabled
        self.gulltoppr = Gulltoppr()
        self.threats_detected = []
        self.scan_history = []
        print("\n" + "="*60)
        print("HEIMDALL - AI PERSONAL ASSISTANT & FIREWALL")
        print("="*60)
        self._speak(random.choice(self.GREETINGS))
    
    def _speak(self, message: str) -> None:
        """
        Simulate voice output.
        
        Args:
            message: The message to speak
        """
        if self.voice_enabled:
            print(f"\n🔊 Heimdall: {message}")
        else:
            print(f"\nHeimdall: {message}")
    
    def speak(self, message: str) -> None:
        """
        Public interface for voice output.
        
        Args:
            message: The message to speak
        """
        self._speak(message)
    
    def think_aloud(self, context: str) -> None:
        """
        Real-time thinking - stream thoughts as they occur.
        
        Args:
            context: The context about what Heimdall is thinking about
        """
        print(f"\n💭 Heimdall's thoughts: {random.choice(self.THINKING_PHRASES)}")
        print(f"   {context}")
        time.sleep(0.3)
    
    def scan_for_threats(self, system_data: Optional[List[Dict]] = None) -> List[Dict]:
        """
        Scan system for potential threats (firewall functionality).
        
        Args:
            system_data: Optional list of system data to scan
            
        Returns:
            List of detected threats
        """
        self.think_aloud("Scanning all realms for threats...")
        
        if system_data is None:
            # Simulate system scanning
            system_data = self._generate_sample_system_data()
        
        detected_threats = []
        
        for item in system_data:
            threat_level = self._analyze_threat_level(item)
            
            if threat_level > 0:
                threat = {
                    'name': item.get('name', 'Unknown'),
                    'severity': self._get_severity_label(threat_level),
                    'location': item.get('location', 'Unknown'),
                    'threat_level': threat_level,
                    'detected_at': datetime.now().isoformat()
                }
                detected_threats.append(threat)
                self.threats_detected.append(threat)
        
        self.scan_history.append({
            'timestamp': datetime.now().isoformat(),
            'threats_found': len(detected_threats),
            'items_scanned': len(system_data)
        })
        
        return detected_threats
    
    def _analyze_threat_level(self, item: Dict) -> int:
        """
        Analyze potential threat level of an item.
        
        Args:
            item: Item to analyze
            
        Returns:
            Threat level (0-10, where 0 is safe)
        """
        # Check for suspicious keywords in item name
        item_name = item.get('name', '').lower()
        for keyword in self.SUSPICIOUS_KEYWORDS:
            if keyword in item_name:
                return random.randint(7, 10)
        
        # Random low-level threats for demonstration
        if random.random() < self.RANDOM_THREAT_PROBABILITY:
            return random.randint(1, 3)
        
        return 0
    
    def _get_severity_label(self, threat_level: int) -> str:
        """Get severity label from threat level."""
        if threat_level >= 8:
            return "CRITICAL"
        elif threat_level >= 5:
            return "HIGH"
        elif threat_level >= 3:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _generate_sample_system_data(self) -> List[Dict]:
        """Generate sample system data for demonstration."""
        return [
            {'name': 'system_update.exe', 'location': '/system/updates'},
            {'name': 'document.pdf', 'location': '/users/documents'},
            {'name': 'image.jpg', 'location': '/users/pictures'},
            {'name': 'suspicious_virus.exe', 'location': '/temp/downloads'},
            {'name': 'data.json', 'location': '/app/data'},
        ]
    
    def dispatch_gulltoppr(self, threats: List[Dict]) -> None:
        """
        Dispatch Gulltoppr to eliminate detected threats.
        
        Args:
            threats: List of threats to eliminate
        """
        if not threats:
            self._speak("No threats detected. My watch continues.")
            return
        
        self._speak(random.choice(self.VIRUS_DETECTED_RESPONSES))
        
        for threat in threats:
            self.gulltoppr.eliminate_threat(threat)
        
        self._speak(random.choice(self.THREAT_ELIMINATED_RESPONSES))
    
    def protect(self) -> None:
        """
        Main protection cycle: scan for threats and dispatch Gulltoppr if needed.
        """
        self.think_aloud("I am ever-vigilant. No threat escapes my sight.")
        
        print("\n" + "-"*60)
        print("INITIATING SYSTEM SCAN")
        print("-"*60)
        
        threats = self.scan_for_threats()
        
        if threats:
            print(f"\n⚠️  {len(threats)} threat(s) detected!")
            for i, threat in enumerate(threats, 1):
                print(f"  {i}. {threat['name']} [{threat['severity']}] @ {threat['location']}")
            
            self.dispatch_gulltoppr(threats)
        else:
            self._speak("All is secure. For now.")
        
        print("\n" + "-"*60)
    
    def status_report(self) -> None:
        """Provide a status report of Heimdall's activities."""
        print("\n" + "="*60)
        print("STATUS REPORT")
        print("="*60)
        
        self._speak("I shall provide my report.")
        
        print(f"\nTotal scans performed: {len(self.scan_history)}")
        print(f"Total threats detected: {len(self.threats_detected)}")
        print(f"Total threats eliminated: {len(self.gulltoppr.eliminated_threats)}")
        
        if self.scan_history:
            latest_scan = self.scan_history[-1]
            print(f"\nLast scan: {latest_scan['timestamp']}")
            print(f"Items scanned: {latest_scan['items_scanned']}")
            print(f"Threats found: {latest_scan['threats_found']}")
        
        print("="*60)


def main():
    """Main entry point for Heimdall."""
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║                        HEIMDALL                            ║
    ║          AI Personal Assistant & Firewall System           ║
    ║                                                            ║
    ║  "I see all. I protect all."                              ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    # Initialize Heimdall
    heimdall = Heimdall(voice_enabled=True)
    
    # Demonstrate real-time thinking
    heimdall.think_aloud("The realms require constant vigilance.")
    
    # Perform protection scan
    heimdall.protect()
    
    # Show status report
    heimdall.status_report()
    
    # Additional demonstration
    print("\n\n" + "="*60)
    print("CUSTOM SCAN DEMONSTRATION")
    print("="*60)
    
    # Custom scan with specific data
    custom_data = [
        {'name': 'banking_app.exe', 'location': '/applications'},
        {'name': 'trojan_malware.exe', 'location': '/temp'},
        {'name': 'backdoor_exploit.dll', 'location': '/system32'},
        {'name': 'readme.txt', 'location': '/documents'},
    ]
    
    heimdall.think_aloud("Scanning custom dataset with heightened scrutiny.")
    threats = heimdall.scan_for_threats(custom_data)
    
    if threats:
        print(f"\n⚠️  {len(threats)} threat(s) detected in custom scan!")
        heimdall.dispatch_gulltoppr(threats)
    
    # Final status
    heimdall.status_report()
    
    print("\n" + "="*60)
    print("Heimdall remains vigilant. The watch never ends.")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
