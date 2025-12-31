#!/usr/bin/env python3
"""
Integration test for Heimdall Firewall Engine
Tests all major features working together
"""

import sys
from firewall_engine import FirewallEngine, FirewallRule, Action, Protocol
from firewall_config import FirewallConfig


def test_integration():
    """Run comprehensive integration test"""
    print("Running Heimdall Firewall Integration Test...")
    print("-" * 70)
    
    # Test 1: Engine creation
    print("\n[Test 1] Creating firewall engine...")
    engine = FirewallEngine(default_action=Action.DENY)
    assert engine.enabled == True
    assert engine.default_action == Action.DENY
    print("✓ Engine created successfully")
    
    # Test 2: Add rules
    print("\n[Test 2] Adding firewall rules...")
    engine.add_rule(FirewallRule(
        name="allow_web",
        action=Action.ALLOW,
        protocol=Protocol.TCP,
        dest_port=80,
        priority=10
    ))
    assert len(engine.rules) == 1
    print("✓ Rules added successfully")
    
    # Test 3: Blacklist/Whitelist
    print("\n[Test 3] Testing IP blacklist and whitelist...")
    engine.add_to_blacklist("192.168.1.100")
    engine.add_to_whitelist("8.8.8.8")
    assert "192.168.1.100" in engine.blacklist_ips
    assert "8.8.8.8" in engine.whitelist_ips
    print("✓ IP lists configured successfully")
    
    # Test 4: Port blocking
    print("\n[Test 4] Testing port blocking...")
    engine.block_port(23)
    assert 23 in engine.blocked_ports
    print("✓ Port blocking works")
    
    # Test 5: Packet processing
    print("\n[Test 5] Testing packet processing...")
    
    # Test whitelist (highest priority)
    packet = {'protocol': 'tcp', 'source_ip': '8.8.8.8', 'dest_ip': '1.1.1.1', 'dest_port': 9999}
    action, reason = engine.process_packet(packet)
    assert action == Action.ALLOW
    assert "whitelist" in reason.lower()
    print("  ✓ Whitelist works (highest priority)")
    
    # Test blacklist
    packet = {'protocol': 'tcp', 'source_ip': '192.168.1.100', 'dest_ip': '1.1.1.1', 'dest_port': 80}
    action, reason = engine.process_packet(packet)
    assert action == Action.DENY
    assert "blacklist" in reason.lower()
    print("  ✓ Blacklist works")
    
    # Test blocked port
    packet = {'protocol': 'tcp', 'source_ip': '10.0.0.1', 'dest_ip': '1.1.1.1', 'dest_port': 23}
    action, reason = engine.process_packet(packet)
    assert action == Action.DENY
    assert "blocked" in reason.lower()
    print("  ✓ Port blocking works")
    
    # Test rule match
    packet = {'protocol': 'tcp', 'source_ip': '10.0.0.1', 'dest_ip': '1.1.1.1', 'dest_port': 80}
    action, reason = engine.process_packet(packet)
    assert action == Action.ALLOW
    assert "allow_web" in reason
    print("  ✓ Rule matching works")
    
    # Test default deny
    packet = {'protocol': 'tcp', 'source_ip': '10.0.0.1', 'dest_ip': '1.1.1.1', 'dest_port': 443}
    action, reason = engine.process_packet(packet)
    assert action == Action.DENY
    assert "default" in reason.lower()
    print("  ✓ Default deny works")
    
    # Test 6: Statistics
    print("\n[Test 6] Testing statistics...")
    stats = engine.get_stats()
    assert stats['total_packets'] == 5
    assert stats['allowed_packets'] == 2
    assert stats['denied_packets'] == 3
    assert stats['whitelist_hits'] == 1
    assert stats['blacklist_hits'] == 1
    print("✓ Statistics tracking works")
    
    # Test 7: Logs
    print("\n[Test 7] Testing logs...")
    logs = engine.get_logs()
    assert len(logs) == 5
    logs_limited = engine.get_logs(limit=2)
    assert len(logs_limited) == 2
    print("✓ Logging works")
    
    # Test 8: Rule management
    print("\n[Test 8] Testing rule management...")
    engine.disable_rule("allow_web")
    packet = {'protocol': 'tcp', 'source_ip': '10.0.0.1', 'dest_ip': '1.1.1.1', 'dest_port': 80}
    action, _ = engine.process_packet(packet)
    assert action == Action.DENY  # Rule disabled
    
    engine.enable_rule("allow_web")
    action, _ = engine.process_packet(packet)
    assert action == Action.ALLOW  # Rule enabled again
    print("✓ Rule enable/disable works")
    
    # Test 9: Configuration save/load
    print("\n[Test 9] Testing configuration save/load...")
    FirewallConfig.save_to_json('/tmp/test_config.json', engine)
    
    new_engine = FirewallEngine(default_action=Action.ALLOW)
    FirewallConfig.load_from_json('/tmp/test_config.json', new_engine)
    
    assert new_engine.default_action == Action.DENY
    assert len(new_engine.rules) == 1
    assert "192.168.1.100" in new_engine.blacklist_ips
    assert "8.8.8.8" in new_engine.whitelist_ips
    print("✓ Configuration save/load works")
    
    # Test 10: Firewall enable/disable
    print("\n[Test 10] Testing firewall enable/disable...")
    engine.disable()
    packet = {'protocol': 'tcp', 'source_ip': '10.0.0.1', 'dest_ip': '1.1.1.1', 'dest_port': 9999}
    action, reason = engine.process_packet(packet)
    assert action == Action.ALLOW
    assert "disabled" in reason.lower()
    
    engine.enable()
    action, _ = engine.process_packet(packet)
    assert action == Action.DENY
    print("✓ Firewall enable/disable works")
    
    # Test 11: Allowed ports (allowlist mode)
    print("\n[Test 11] Testing allowed ports (allowlist mode)...")
    engine2 = FirewallEngine(default_action=Action.DENY)
    engine2.allow_port(80)
    engine2.allow_port(443)
    
    packet1 = {'protocol': 'tcp', 'source_ip': '10.0.0.1', 'dest_ip': '1.1.1.1', 'dest_port': 80}
    action1, _ = engine2.process_packet(packet1)
    assert action1 == Action.ALLOW
    
    packet2 = {'protocol': 'tcp', 'source_ip': '10.0.0.1', 'dest_ip': '1.1.1.1', 'dest_port': 23}
    action2, _ = engine2.process_packet(packet2)
    assert action2 == Action.DENY
    print("✓ Allowed ports (allowlist mode) works")
    
    print("\n" + "-" * 70)
    print("✅ All integration tests passed!")
    print(f"Total tests: 11")
    print(f"Total packets processed: {engine.get_stats()['total_packets']}")
    return 0


if __name__ == '__main__':
    try:
        sys.exit(test_integration())
    except AssertionError as e:
        print(f"\n❌ Integration test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
