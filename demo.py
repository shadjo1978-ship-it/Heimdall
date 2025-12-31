#!/usr/bin/env python3
"""
Demo script showing Heimdall Firewall Engine in action
"""

from firewall_engine import FirewallEngine, FirewallRule, Action, Protocol
from firewall_config import FirewallConfig


def print_separator():
    print("\n" + "=" * 70 + "\n")


def main():
    print("Heimdall Firewall Engine - Demo")
    print_separator()
    
    # Create firewall with default deny policy
    print("Creating firewall with default DENY policy...")
    firewall = FirewallEngine(default_action=Action.DENY)
    print(f"✓ Firewall created (default action: {firewall.default_action.value})")
    
    print_separator()
    
    # Add some basic rules
    print("Adding firewall rules...")
    
    # Allow HTTP traffic
    firewall.add_rule(FirewallRule(
        name="allow_http",
        action=Action.ALLOW,
        protocol=Protocol.TCP,
        dest_port=80,
        priority=10
    ))
    
    # Allow HTTPS traffic
    firewall.add_rule(FirewallRule(
        name="allow_https",
        action=Action.ALLOW,
        protocol=Protocol.TCP,
        dest_port=443,
        priority=10
    ))
    
    # Block SSH from external sources
    firewall.add_rule(FirewallRule(
        name="block_external_ssh",
        action=Action.DENY,
        protocol=Protocol.TCP,
        dest_port=22,
        source_ip="0.0.0.0/0",
        priority=5
    ))
    
    print(f"✓ Added {len(firewall.rules)} rules")
    
    print_separator()
    
    # Add IP blacklist
    print("Configuring IP blacklist...")
    firewall.add_to_blacklist("192.168.1.100")
    firewall.add_to_blacklist("10.0.0.50")
    print(f"✓ Blacklisted {len(firewall.blacklist_ips)} IPs")
    
    print_separator()
    
    # Add trusted IPs to whitelist
    print("Configuring IP whitelist...")
    firewall.add_to_whitelist("8.8.8.8")  # Google DNS
    firewall.add_to_whitelist("1.1.1.1")  # Cloudflare DNS
    print(f"✓ Whitelisted {len(firewall.whitelist_ips)} IPs")
    
    print_separator()
    
    # Block dangerous ports
    print("Blocking dangerous ports...")
    firewall.block_port(23)   # Telnet
    firewall.block_port(21)   # FTP
    firewall.block_port(445)  # SMB
    print(f"✓ Blocked {len(firewall.blocked_ports)} ports")
    
    print_separator()
    
    # Test some packets
    print("Testing packets against firewall rules...\n")
    
    test_packets = [
        {
            'name': 'HTTP Request',
            'packet': {
                'protocol': 'tcp',
                'source_ip': '203.0.113.10',
                'dest_ip': '192.168.1.1',
                'dest_port': 80
            }
        },
        {
            'name': 'HTTPS Request',
            'packet': {
                'protocol': 'tcp',
                'source_ip': '203.0.113.10',
                'dest_ip': '192.168.1.1',
                'dest_port': 443
            }
        },
        {
            'name': 'SSH from Blacklisted IP',
            'packet': {
                'protocol': 'tcp',
                'source_ip': '192.168.1.100',
                'dest_ip': '192.168.1.1',
                'dest_port': 22
            }
        },
        {
            'name': 'Request from Whitelisted IP',
            'packet': {
                'protocol': 'tcp',
                'source_ip': '8.8.8.8',
                'dest_ip': '192.168.1.1',
                'dest_port': 9999
            }
        },
        {
            'name': 'Telnet (Blocked Port)',
            'packet': {
                'protocol': 'tcp',
                'source_ip': '203.0.113.10',
                'dest_ip': '192.168.1.1',
                'dest_port': 23
            }
        },
        {
            'name': 'Unknown Protocol/Port',
            'packet': {
                'protocol': 'tcp',
                'source_ip': '203.0.113.10',
                'dest_ip': '192.168.1.1',
                'dest_port': 9999
            }
        }
    ]
    
    for test in test_packets:
        action, reason = firewall.process_packet(test['packet'])
        status = "✓ ALLOWED" if action == Action.ALLOW else "✗ DENIED"
        print(f"{test['name']:<30} {status:<15} ({reason})")
    
    print_separator()
    
    # Show statistics
    print("Firewall Statistics:")
    stats = firewall.get_stats()
    print(f"  Total packets processed: {stats['total_packets']}")
    print(f"  Packets allowed: {stats['allowed_packets']}")
    print(f"  Packets denied: {stats['denied_packets']}")
    print(f"  Blacklist hits: {stats['blacklist_hits']}")
    print(f"  Whitelist hits: {stats['whitelist_hits']}")
    
    print_separator()
    
    # Show recent logs
    print("Recent packet logs (last 3):")
    logs = firewall.get_logs(limit=3)
    for log in logs:
        print(f"  {log}")
    
    print_separator()
    
    # Save configuration
    print("Saving configuration to demo_config.json...")
    FirewallConfig.save_to_json('demo_config.json', firewall)
    print("✓ Configuration saved")
    
    print_separator()
    
    print("Demo completed successfully!")
    print("\nYou can now:")
    print("  - View the saved config: cat demo_config.json")
    print("  - Load it with CLI: ./firewall_cli.py load-config demo_config.json")
    print("  - View all rules: ./firewall_cli.py list-rules")
    print("  - Test a packet: ./firewall_cli.py test-packet --help")


if __name__ == '__main__':
    main()
