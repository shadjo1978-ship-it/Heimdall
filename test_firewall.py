"""
Unit tests for the Heimdall Firewall Engine
"""

import unittest
from firewall_engine import FirewallEngine, FirewallRule, Action, Protocol


class TestFirewallRule(unittest.TestCase):
    """Test FirewallRule class"""
    
    def test_create_basic_rule(self):
        """Test creating a basic rule"""
        rule = FirewallRule(
            name="test_rule",
            action=Action.ALLOW,
            protocol=Protocol.TCP
        )
        self.assertEqual(rule.name, "test_rule")
        self.assertEqual(rule.action, Action.ALLOW)
        self.assertEqual(rule.protocol, Protocol.TCP)
        self.assertTrue(rule.enabled)
    
    def test_rule_with_ip_addresses(self):
        """Test rule with IP addresses"""
        rule = FirewallRule(
            name="ip_rule",
            action=Action.DENY,
            source_ip="192.168.1.0/24",
            dest_ip="10.0.0.1"
        )
        self.assertEqual(rule.source_ip, "192.168.1.0/24")
        self.assertEqual(rule.dest_ip, "10.0.0.1")
    
    def test_invalid_source_ip(self):
        """Test that invalid source IP raises error"""
        with self.assertRaises(ValueError):
            FirewallRule(
                name="bad_rule",
                action=Action.ALLOW,
                source_ip="invalid_ip"
            )
    
    def test_invalid_dest_ip(self):
        """Test that invalid destination IP raises error"""
        with self.assertRaises(ValueError):
            FirewallRule(
                name="bad_rule",
                action=Action.ALLOW,
                dest_ip="999.999.999.999"
            )
    
    def test_rule_matches_protocol(self):
        """Test rule matching on protocol"""
        rule = FirewallRule(
            name="tcp_rule",
            action=Action.ALLOW,
            protocol=Protocol.TCP
        )
        
        tcp_packet = {'protocol': 'tcp', 'source_ip': '1.2.3.4', 'dest_ip': '5.6.7.8'}
        udp_packet = {'protocol': 'udp', 'source_ip': '1.2.3.4', 'dest_ip': '5.6.7.8'}
        
        self.assertTrue(rule.matches(tcp_packet))
        self.assertFalse(rule.matches(udp_packet))
    
    def test_rule_matches_source_ip(self):
        """Test rule matching on source IP"""
        rule = FirewallRule(
            name="ip_rule",
            action=Action.DENY,
            source_ip="192.168.1.0/24"
        )
        
        matching_packet = {'source_ip': '192.168.1.50', 'dest_ip': '8.8.8.8', 'protocol': 'tcp'}
        non_matching_packet = {'source_ip': '10.0.0.1', 'dest_ip': '8.8.8.8', 'protocol': 'tcp'}
        
        self.assertTrue(rule.matches(matching_packet))
        self.assertFalse(rule.matches(non_matching_packet))
    
    def test_rule_matches_port(self):
        """Test rule matching on ports"""
        rule = FirewallRule(
            name="port_rule",
            action=Action.ALLOW,
            dest_port=80
        )
        
        matching_packet = {'source_ip': '1.2.3.4', 'dest_ip': '5.6.7.8', 'dest_port': 80, 'protocol': 'tcp'}
        non_matching_packet = {'source_ip': '1.2.3.4', 'dest_ip': '5.6.7.8', 'dest_port': 443, 'protocol': 'tcp'}
        
        self.assertTrue(rule.matches(matching_packet))
        self.assertFalse(rule.matches(non_matching_packet))
    
    def test_disabled_rule_doesnt_match(self):
        """Test that disabled rules don't match"""
        rule = FirewallRule(
            name="disabled_rule",
            action=Action.ALLOW,
            enabled=False
        )
        
        packet = {'source_ip': '1.2.3.4', 'dest_ip': '5.6.7.8', 'protocol': 'tcp'}
        self.assertFalse(rule.matches(packet))


class TestFirewallEngine(unittest.TestCase):
    """Test FirewallEngine class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.engine = FirewallEngine(default_action=Action.DENY)
    
    def test_default_action(self):
        """Test default action when no rules match"""
        packet = {'source_ip': '1.2.3.4', 'dest_ip': '5.6.7.8', 'protocol': 'tcp'}
        action, reason = self.engine.process_packet(packet)
        
        self.assertEqual(action, Action.DENY)
        self.assertIn("default", reason.lower())
    
    def test_add_and_match_rule(self):
        """Test adding a rule and matching a packet"""
        rule = FirewallRule(
            name="allow_http",
            action=Action.ALLOW,
            protocol=Protocol.TCP,
            dest_port=80
        )
        self.engine.add_rule(rule)
        
        packet = {'source_ip': '1.2.3.4', 'dest_ip': '5.6.7.8', 'dest_port': 80, 'protocol': 'tcp'}
        action, reason = self.engine.process_packet(packet)
        
        self.assertEqual(action, Action.ALLOW)
        self.assertIn("allow_http", reason)
    
    def test_rule_priority(self):
        """Test that rules are evaluated in priority order"""
        # Lower priority number = higher priority
        high_priority_rule = FirewallRule(
            name="high_priority",
            action=Action.DENY,
            protocol=Protocol.TCP,
            priority=10
        )
        low_priority_rule = FirewallRule(
            name="low_priority",
            action=Action.ALLOW,
            protocol=Protocol.TCP,
            priority=100
        )
        
        self.engine.add_rule(low_priority_rule)
        self.engine.add_rule(high_priority_rule)
        
        packet = {'source_ip': '1.2.3.4', 'dest_ip': '5.6.7.8', 'protocol': 'tcp'}
        action, reason = self.engine.process_packet(packet)
        
        # High priority rule should match first
        self.assertEqual(action, Action.DENY)
        self.assertIn("high_priority", reason)
    
    def test_blacklist(self):
        """Test IP blacklist functionality"""
        self.engine.add_to_blacklist('1.2.3.4')
        
        packet = {'source_ip': '1.2.3.4', 'dest_ip': '5.6.7.8', 'protocol': 'tcp'}
        action, reason = self.engine.process_packet(packet)
        
        self.assertEqual(action, Action.DENY)
        self.assertIn("blacklist", reason.lower())
    
    def test_whitelist(self):
        """Test IP whitelist functionality"""
        self.engine.add_to_whitelist('1.2.3.4')
        
        packet = {'source_ip': '1.2.3.4', 'dest_ip': '5.6.7.8', 'protocol': 'tcp'}
        action, reason = self.engine.process_packet(packet)
        
        self.assertEqual(action, Action.ALLOW)
        self.assertIn("whitelist", reason.lower())
    
    def test_whitelist_overrides_blacklist(self):
        """Test that whitelist has higher priority than blacklist"""
        self.engine.add_to_blacklist('1.2.3.4')
        self.engine.add_to_whitelist('1.2.3.4')
        
        packet = {'source_ip': '1.2.3.4', 'dest_ip': '5.6.7.8', 'protocol': 'tcp'}
        action, reason = self.engine.process_packet(packet)
        
        self.assertEqual(action, Action.ALLOW)
        self.assertIn("whitelist", reason.lower())
    
    def test_blocked_port(self):
        """Test port blocking functionality"""
        self.engine.block_port(23)  # Block telnet
        
        packet = {'source_ip': '1.2.3.4', 'dest_ip': '5.6.7.8', 'dest_port': 23, 'protocol': 'tcp'}
        action, reason = self.engine.process_packet(packet)
        
        self.assertEqual(action, Action.DENY)
        self.assertIn("blocked", reason.lower())
    
    def test_allowed_ports(self):
        """Test allowed ports functionality"""
        self.engine.allow_port(80)
        self.engine.allow_port(443)
        
        # Port in allowed list should be allowed
        packet1 = {'source_ip': '1.2.3.4', 'dest_ip': '5.6.7.8', 'dest_port': 80, 'protocol': 'tcp'}
        action1, _ = self.engine.process_packet(packet1)
        self.assertEqual(action1, Action.ALLOW)
        
        # Port not in allowed list should be denied
        packet2 = {'source_ip': '1.2.3.4', 'dest_ip': '5.6.7.8', 'dest_port': 23, 'protocol': 'tcp'}
        action2, reason2 = self.engine.process_packet(packet2)
        self.assertEqual(action2, Action.DENY)
        self.assertIn("not in allowlist", reason2.lower())
    
    def test_remove_rule(self):
        """Test removing a rule"""
        rule = FirewallRule(name="temp_rule", action=Action.ALLOW)
        self.engine.add_rule(rule)
        
        self.assertTrue(self.engine.remove_rule("temp_rule"))
        self.assertFalse(self.engine.remove_rule("temp_rule"))  # Already removed
    
    def test_enable_disable_rule(self):
        """Test enabling and disabling rules"""
        rule = FirewallRule(name="toggle_rule", action=Action.ALLOW, protocol=Protocol.TCP)
        self.engine.add_rule(rule)
        
        # Disable the rule
        self.assertTrue(self.engine.disable_rule("toggle_rule"))
        
        packet = {'source_ip': '1.2.3.4', 'dest_ip': '5.6.7.8', 'protocol': 'tcp'}
        action, _ = self.engine.process_packet(packet)
        self.assertEqual(action, Action.DENY)  # Rule disabled, so default action
        
        # Enable the rule
        self.assertTrue(self.engine.enable_rule("toggle_rule"))
        action, _ = self.engine.process_packet(packet)
        self.assertEqual(action, Action.ALLOW)  # Rule enabled again
    
    def test_enable_disable_firewall(self):
        """Test enabling and disabling the entire firewall"""
        self.engine.disable()
        
        packet = {'source_ip': '1.2.3.4', 'dest_ip': '5.6.7.8', 'protocol': 'tcp'}
        action, reason = self.engine.process_packet(packet)
        
        self.assertEqual(action, Action.ALLOW)
        self.assertIn("disabled", reason.lower())
        
        self.engine.enable()
        action, _ = self.engine.process_packet(packet)
        self.assertEqual(action, Action.DENY)  # Back to default deny
    
    def test_statistics(self):
        """Test statistics tracking"""
        self.engine.add_to_whitelist('1.2.3.4')
        self.engine.add_to_blacklist('5.6.7.8')
        
        packet1 = {'source_ip': '1.2.3.4', 'dest_ip': '8.8.8.8', 'protocol': 'tcp'}
        packet2 = {'source_ip': '5.6.7.8', 'dest_ip': '8.8.8.8', 'protocol': 'tcp'}
        packet3 = {'source_ip': '9.9.9.9', 'dest_ip': '8.8.8.8', 'protocol': 'tcp'}
        
        self.engine.process_packet(packet1)  # Whitelist hit
        self.engine.process_packet(packet2)  # Blacklist hit
        self.engine.process_packet(packet3)  # Default deny
        
        stats = self.engine.get_stats()
        self.assertEqual(stats['total_packets'], 3)
        self.assertEqual(stats['allowed_packets'], 1)
        self.assertEqual(stats['denied_packets'], 2)
        self.assertEqual(stats['whitelist_hits'], 1)
        self.assertEqual(stats['blacklist_hits'], 1)
    
    def test_packet_logging(self):
        """Test packet logging"""
        packet = {'source_ip': '1.2.3.4', 'dest_ip': '5.6.7.8', 'protocol': 'tcp'}
        self.engine.process_packet(packet)
        
        logs = self.engine.get_logs()
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0].packet['source_ip'], '1.2.3.4')
        self.assertEqual(logs[0].action, Action.DENY)
    
    def test_clear_logs(self):
        """Test clearing logs"""
        packet = {'source_ip': '1.2.3.4', 'dest_ip': '5.6.7.8', 'protocol': 'tcp'}
        self.engine.process_packet(packet)
        
        self.engine.clear_logs()
        logs = self.engine.get_logs()
        self.assertEqual(len(logs), 0)
    
    def test_get_logs_with_limit(self):
        """Test getting logs with limit"""
        for i in range(10):
            packet = {'source_ip': f'{i}.{i}.{i}.{i}', 'dest_ip': '5.6.7.8', 'protocol': 'tcp'}
            self.engine.process_packet(packet)
        
        logs = self.engine.get_logs(limit=3)
        self.assertEqual(len(logs), 3)
    
    def test_invalid_ip_blacklist(self):
        """Test that invalid IPs can't be added to blacklist"""
        with self.assertRaises(ValueError):
            self.engine.add_to_blacklist("invalid_ip")
    
    def test_invalid_ip_whitelist(self):
        """Test that invalid IPs can't be added to whitelist"""
        with self.assertRaises(ValueError):
            self.engine.add_to_whitelist("999.999.999.999")
    
    def test_invalid_port_block(self):
        """Test that invalid ports can't be blocked"""
        with self.assertRaises(ValueError):
            self.engine.block_port(70000)
        
        with self.assertRaises(ValueError):
            self.engine.block_port(-1)


if __name__ == '__main__':
    unittest.main()
