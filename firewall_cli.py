#!/usr/bin/env python3
"""
Heimdall Firewall CLI
Command-line interface for managing the firewall engine.
"""

import sys
import argparse
from firewall_engine import FirewallEngine, FirewallRule, Action, Protocol
from firewall_config import FirewallConfig


def create_parser():
    """Create the argument parser"""
    parser = argparse.ArgumentParser(
        description='Heimdall Firewall CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Rule management commands
    add_rule_parser = subparsers.add_parser('add-rule', help='Add a firewall rule')
    add_rule_parser.add_argument('name', help='Rule name')
    add_rule_parser.add_argument('action', choices=['allow', 'deny'], help='Action to take')
    add_rule_parser.add_argument('--protocol', choices=['tcp', 'udp', 'icmp', 'any'], default='any', help='Protocol')
    add_rule_parser.add_argument('--source-ip', help='Source IP address or CIDR')
    add_rule_parser.add_argument('--dest-ip', help='Destination IP address or CIDR')
    add_rule_parser.add_argument('--source-port', type=int, help='Source port')
    add_rule_parser.add_argument('--dest-port', type=int, help='Destination port')
    add_rule_parser.add_argument('--priority', type=int, default=100, help='Rule priority (lower = higher priority)')
    
    remove_rule_parser = subparsers.add_parser('remove-rule', help='Remove a firewall rule')
    remove_rule_parser.add_argument('name', help='Rule name to remove')
    
    enable_rule_parser = subparsers.add_parser('enable-rule', help='Enable a firewall rule')
    enable_rule_parser.add_argument('name', help='Rule name to enable')
    
    disable_rule_parser = subparsers.add_parser('disable-rule', help='Disable a firewall rule')
    disable_rule_parser.add_argument('name', help='Rule name to disable')
    
    # IP management commands
    blacklist_parser = subparsers.add_parser('blacklist', help='Add IP to blacklist')
    blacklist_parser.add_argument('ip', help='IP address to blacklist')
    
    unblacklist_parser = subparsers.add_parser('unblacklist', help='Remove IP from blacklist')
    unblacklist_parser.add_argument('ip', help='IP address to remove from blacklist')
    
    whitelist_parser = subparsers.add_parser('whitelist', help='Add IP to whitelist')
    whitelist_parser.add_argument('ip', help='IP address to whitelist')
    
    unwhitelist_parser = subparsers.add_parser('unwhitelist', help='Remove IP from whitelist')
    unwhitelist_parser.add_argument('ip', help='IP address to remove from whitelist')
    
    # Port management commands
    block_port_parser = subparsers.add_parser('block-port', help='Block a port')
    block_port_parser.add_argument('port', type=int, help='Port number to block')
    
    unblock_port_parser = subparsers.add_parser('unblock-port', help='Unblock a port')
    unblock_port_parser.add_argument('port', type=int, help='Port number to unblock')
    
    allow_port_parser = subparsers.add_parser('allow-port', help='Allow a port')
    allow_port_parser.add_argument('port', type=int, help='Port number to allow')
    
    # Packet testing
    test_packet_parser = subparsers.add_parser('test-packet', help='Test a packet against firewall rules')
    test_packet_parser.add_argument('--protocol', default='tcp', help='Protocol')
    test_packet_parser.add_argument('--source-ip', required=True, help='Source IP address')
    test_packet_parser.add_argument('--dest-ip', required=True, help='Destination IP address')
    test_packet_parser.add_argument('--source-port', type=int, help='Source port')
    test_packet_parser.add_argument('--dest-port', type=int, help='Destination port')
    
    # Status and information
    subparsers.add_parser('list-rules', help='List all firewall rules')
    subparsers.add_parser('stats', help='Show firewall statistics')
    subparsers.add_parser('status', help='Show firewall status')
    
    logs_parser = subparsers.add_parser('logs', help='Show packet logs')
    logs_parser.add_argument('--limit', type=int, help='Number of recent logs to show')
    
    # Configuration management
    load_config_parser = subparsers.add_parser('load-config', help='Load configuration from file')
    load_config_parser.add_argument('filepath', help='Path to configuration file')
    load_config_parser.add_argument('--format', choices=['json', 'yaml'], default='json', help='File format')
    
    save_config_parser = subparsers.add_parser('save-config', help='Save configuration to file')
    save_config_parser.add_argument('filepath', help='Path to save configuration')
    save_config_parser.add_argument('--format', choices=['json', 'yaml'], default='json', help='File format')
    
    # Firewall control
    subparsers.add_parser('enable', help='Enable the firewall')
    subparsers.add_parser('disable', help='Disable the firewall')
    
    return parser


def main():
    """Main CLI entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Initialize firewall engine
    engine = FirewallEngine(default_action=Action.DENY)
    
    try:
        # Handle commands
        if args.command == 'add-rule':
            rule = FirewallRule(
                name=args.name,
                action=Action(args.action),
                protocol=Protocol(args.protocol),
                source_ip=args.source_ip,
                dest_ip=args.dest_ip,
                source_port=args.source_port,
                dest_port=args.dest_port,
                priority=args.priority
            )
            engine.add_rule(rule)
            print(f"Rule '{args.name}' added successfully")
        
        elif args.command == 'remove-rule':
            if engine.remove_rule(args.name):
                print(f"Rule '{args.name}' removed successfully")
            else:
                print(f"Rule '{args.name}' not found")
                return 1
        
        elif args.command == 'enable-rule':
            if engine.enable_rule(args.name):
                print(f"Rule '{args.name}' enabled successfully")
            else:
                print(f"Rule '{args.name}' not found")
                return 1
        
        elif args.command == 'disable-rule':
            if engine.disable_rule(args.name):
                print(f"Rule '{args.name}' disabled successfully")
            else:
                print(f"Rule '{args.name}' not found")
                return 1
        
        elif args.command == 'blacklist':
            engine.add_to_blacklist(args.ip)
            print(f"IP '{args.ip}' added to blacklist")
        
        elif args.command == 'unblacklist':
            if engine.remove_from_blacklist(args.ip):
                print(f"IP '{args.ip}' removed from blacklist")
            else:
                print(f"IP '{args.ip}' not in blacklist")
                return 1
        
        elif args.command == 'whitelist':
            engine.add_to_whitelist(args.ip)
            print(f"IP '{args.ip}' added to whitelist")
        
        elif args.command == 'unwhitelist':
            if engine.remove_from_whitelist(args.ip):
                print(f"IP '{args.ip}' removed from whitelist")
            else:
                print(f"IP '{args.ip}' not in whitelist")
                return 1
        
        elif args.command == 'block-port':
            engine.block_port(args.port)
            print(f"Port {args.port} blocked")
        
        elif args.command == 'unblock-port':
            if engine.unblock_port(args.port):
                print(f"Port {args.port} unblocked")
            else:
                print(f"Port {args.port} not in blocked list")
                return 1
        
        elif args.command == 'allow-port':
            engine.allow_port(args.port)
            print(f"Port {args.port} allowed")
        
        elif args.command == 'test-packet':
            packet = {
                'protocol': args.protocol,
                'source_ip': args.source_ip,
                'dest_ip': args.dest_ip,
                'source_port': args.source_port,
                'dest_port': args.dest_port
            }
            action, reason = engine.process_packet(packet)
            print(f"Packet would be {action.value.upper()}: {reason}")
        
        elif args.command == 'list-rules':
            rules = engine.get_rules()
            if not rules:
                print("No rules configured")
            else:
                print(f"{'Name':<20} {'Action':<10} {'Protocol':<10} {'Priority':<10} {'Enabled':<10}")
                print("-" * 70)
                for rule in rules:
                    print(f"{rule.name:<20} {rule.action.value:<10} {rule.protocol.value:<10} {rule.priority:<10} {rule.enabled}")
                    if rule.source_ip or rule.dest_ip:
                        print(f"  Source: {rule.source_ip or 'any':<15} Dest: {rule.dest_ip or 'any'}")
                    if rule.source_port is not None or rule.dest_port is not None:
                        print(f"  Source Port: {rule.source_port or 'any':<10} Dest Port: {rule.dest_port or 'any'}")
        
        elif args.command == 'stats':
            stats = engine.get_stats()
            print("Firewall Statistics:")
            print(f"  Total packets: {stats['total_packets']}")
            print(f"  Allowed packets: {stats['allowed_packets']}")
            print(f"  Denied packets: {stats['denied_packets']}")
            print(f"  Blacklist hits: {stats['blacklist_hits']}")
            print(f"  Whitelist hits: {stats['whitelist_hits']}")
        
        elif args.command == 'status':
            print(f"Firewall Status: {'ENABLED' if engine.enabled else 'DISABLED'}")
            print(f"Default Action: {engine.default_action.value.upper()}")
            print(f"Active Rules: {len([r for r in engine.rules if r.enabled])}/{len(engine.rules)}")
            print(f"Blacklisted IPs: {len(engine.blacklist_ips)}")
            print(f"Whitelisted IPs: {len(engine.whitelist_ips)}")
            print(f"Blocked Ports: {len(engine.blocked_ports)}")
            print(f"Allowed Ports: {len(engine.allowed_ports)}")
        
        elif args.command == 'logs':
            logs = engine.get_logs(limit=args.limit)
            if not logs:
                print("No logs available")
            else:
                for log in logs:
                    print(log)
        
        elif args.command == 'load-config':
            if args.format == 'json':
                FirewallConfig.load_from_json(args.filepath, engine)
            else:
                FirewallConfig.load_from_yaml(args.filepath, engine)
            print(f"Configuration loaded from {args.filepath}")
        
        elif args.command == 'save-config':
            if args.format == 'json':
                FirewallConfig.save_to_json(args.filepath, engine)
            else:
                FirewallConfig.save_to_yaml(args.filepath, engine)
            print(f"Configuration saved to {args.filepath}")
        
        elif args.command == 'enable':
            engine.enable()
            print("Firewall enabled")
        
        elif args.command == 'disable':
            engine.disable()
            print("Firewall disabled")
        
        return 0
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
