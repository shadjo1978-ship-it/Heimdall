"""
Heimdall Firewall Engine
A lightweight firewall engine for packet filtering and network security.
"""

import logging
import ipaddress
from typing import List, Dict, Set, Optional, Tuple
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime


class Action(Enum):
    """Firewall actions"""
    ALLOW = "allow"
    DENY = "deny"


class Protocol(Enum):
    """Network protocols"""
    TCP = "tcp"
    UDP = "udp"
    ICMP = "icmp"
    ANY = "any"


@dataclass
class FirewallRule:
    """Represents a firewall rule"""
    name: str
    action: Action
    protocol: Protocol = Protocol.ANY
    source_ip: Optional[str] = None
    dest_ip: Optional[str] = None
    source_port: Optional[int] = None
    dest_port: Optional[int] = None
    priority: int = 100
    enabled: bool = True
    
    def __post_init__(self):
        """Validate IP addresses"""
        if self.source_ip:
            try:
                ipaddress.ip_network(self.source_ip, strict=False)
            except ValueError as e:
                raise ValueError(f"Invalid source IP: {self.source_ip}") from e
        
        if self.dest_ip:
            try:
                ipaddress.ip_network(self.dest_ip, strict=False)
            except ValueError as e:
                raise ValueError(f"Invalid destination IP: {self.dest_ip}") from e
    
    def matches(self, packet: Dict) -> bool:
        """Check if a packet matches this rule"""
        if not self.enabled:
            return False
        
        # Check protocol
        if self.protocol != Protocol.ANY:
            if packet.get('protocol', '').lower() != self.protocol.value:
                return False
        
        # Check source IP
        if self.source_ip:
            try:
                src_ip = ipaddress.ip_address(packet.get('source_ip', ''))
                src_network = ipaddress.ip_network(self.source_ip, strict=False)
                if src_ip not in src_network:
                    return False
            except (ValueError, KeyError):
                return False
        
        # Check destination IP
        if self.dest_ip:
            try:
                dst_ip = ipaddress.ip_address(packet.get('dest_ip', ''))
                dst_network = ipaddress.ip_network(self.dest_ip, strict=False)
                if dst_ip not in dst_network:
                    return False
            except (ValueError, KeyError):
                return False
        
        # Check source port
        if self.source_port is not None:
            if packet.get('source_port') != self.source_port:
                return False
        
        # Check destination port
        if self.dest_port is not None:
            if packet.get('dest_port') != self.dest_port:
                return False
        
        return True


@dataclass
class PacketLog:
    """Represents a logged packet"""
    timestamp: datetime
    action: Action
    packet: Dict
    rule_name: str
    
    def __str__(self):
        return (f"[{self.timestamp.isoformat()}] {self.action.value.upper()} - "
                f"Rule: {self.rule_name} - "
                f"{self.packet.get('protocol', 'UNKNOWN')} "
                f"{self.packet.get('source_ip', '?')}:{self.packet.get('source_port', '?')} -> "
                f"{self.packet.get('dest_ip', '?')}:{self.packet.get('dest_port', '?')}")


class FirewallEngine:
    """
    Main firewall engine for packet filtering.
    
    The engine maintains a list of rules and processes packets against them.
    Rules are evaluated in priority order (lower number = higher priority).
    """
    
    def __init__(self, default_action: Action = Action.DENY):
        """
        Initialize the firewall engine.
        
        Args:
            default_action: Default action when no rules match (default: DENY)
        """
        self.default_action = default_action
        self.rules: List[FirewallRule] = []
        self.packet_logs: List[PacketLog] = []
        self.blacklist_ips: Set[str] = set()
        self.whitelist_ips: Set[str] = set()
        self.blocked_ports: Set[int] = set()
        self.allowed_ports: Set[int] = set()
        self.enabled = True
        
        # Statistics
        self.stats = {
            'total_packets': 0,
            'allowed_packets': 0,
            'denied_packets': 0,
            'blacklist_hits': 0,
            'whitelist_hits': 0
        }
        
        # Setup logging
        self.logger = logging.getLogger('FirewallEngine')
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def add_rule(self, rule: FirewallRule) -> None:
        """
        Add a firewall rule.
        
        Args:
            rule: The firewall rule to add
        """
        self.rules.append(rule)
        # Sort rules by priority (lower number = higher priority)
        self.rules.sort(key=lambda r: r.priority)
        self.logger.info(f"Added rule: {rule.name} (priority: {rule.priority})")
    
    def remove_rule(self, rule_name: str) -> bool:
        """
        Remove a firewall rule by name.
        
        Args:
            rule_name: Name of the rule to remove
            
        Returns:
            True if rule was removed, False if not found
        """
        for i, rule in enumerate(self.rules):
            if rule.name == rule_name:
                removed_rule = self.rules.pop(i)
                self.logger.info(f"Removed rule: {removed_rule.name}")
                return True
        return False
    
    def enable_rule(self, rule_name: str) -> bool:
        """Enable a rule by name"""
        for rule in self.rules:
            if rule.name == rule_name:
                rule.enabled = True
                self.logger.info(f"Enabled rule: {rule_name}")
                return True
        return False
    
    def disable_rule(self, rule_name: str) -> bool:
        """Disable a rule by name"""
        for rule in self.rules:
            if rule.name == rule_name:
                rule.enabled = False
                self.logger.info(f"Disabled rule: {rule_name}")
                return True
        return False
    
    def add_to_blacklist(self, ip: str) -> None:
        """Add an IP address to the blacklist"""
        try:
            # Validate IP
            ipaddress.ip_address(ip)
            self.blacklist_ips.add(ip)
            self.logger.info(f"Added {ip} to blacklist")
        except ValueError as e:
            raise ValueError(f"Invalid IP address: {ip}") from e
    
    def remove_from_blacklist(self, ip: str) -> bool:
        """Remove an IP address from the blacklist"""
        if ip in self.blacklist_ips:
            self.blacklist_ips.remove(ip)
            self.logger.info(f"Removed {ip} from blacklist")
            return True
        return False
    
    def add_to_whitelist(self, ip: str) -> None:
        """Add an IP address to the whitelist"""
        try:
            # Validate IP
            ipaddress.ip_address(ip)
            self.whitelist_ips.add(ip)
            self.logger.info(f"Added {ip} to whitelist")
        except ValueError as e:
            raise ValueError(f"Invalid IP address: {ip}") from e
    
    def remove_from_whitelist(self, ip: str) -> bool:
        """Remove an IP address from the whitelist"""
        if ip in self.whitelist_ips:
            self.whitelist_ips.remove(ip)
            self.logger.info(f"Removed {ip} from whitelist")
            return True
        return False
    
    def block_port(self, port: int) -> None:
        """Block a specific port"""
        if not 0 <= port <= 65535:
            raise ValueError(f"Invalid port number: {port}")
        self.blocked_ports.add(port)
        self.logger.info(f"Blocked port: {port}")
    
    def unblock_port(self, port: int) -> bool:
        """Unblock a specific port"""
        if port in self.blocked_ports:
            self.blocked_ports.remove(port)
            self.logger.info(f"Unblocked port: {port}")
            return True
        return False
    
    def allow_port(self, port: int) -> None:
        """
        Allow a specific port (port allowlist mode).
        
        When allowed_ports is configured (non-empty), the firewall operates in
        port allowlist mode: only packets destined to ports in this set are
        allowed, all other ports are denied immediately.
        
        Note: Packets without a dest_port field will bypass this check and
        proceed to rule evaluation.
        
        Args:
            port: Port number to allow (0-65535)
        """
        if not 0 <= port <= 65535:
            raise ValueError(f"Invalid port number: {port}")
        self.allowed_ports.add(port)
        self.logger.info(f"Allowed port: {port}")
    
    def process_packet(self, packet: Dict) -> Tuple[Action, str]:
        """
        Process a packet through the firewall.
        
        Args:
            packet: Dictionary containing packet information with keys:
                   - protocol: str (tcp, udp, icmp, etc.)
                   - source_ip: str
                   - dest_ip: str
                   - source_port: int (optional)
                   - dest_port: int (optional)
        
        Returns:
            Tuple of (Action, reason) indicating whether to allow or deny the packet
        """
        if not self.enabled:
            return Action.ALLOW, "Firewall disabled"
        
        self.stats['total_packets'] += 1
        
        # Check whitelist first (highest priority)
        source_ip = packet.get('source_ip', '')
        if source_ip in self.whitelist_ips:
            self.stats['whitelist_hits'] += 1
            self.stats['allowed_packets'] += 1
            self._log_packet(Action.ALLOW, packet, "IP whitelist")
            return Action.ALLOW, "IP whitelist"
        
        # Check blacklist
        if source_ip in self.blacklist_ips:
            self.stats['blacklist_hits'] += 1
            self.stats['denied_packets'] += 1
            self._log_packet(Action.DENY, packet, "IP blacklist")
            return Action.DENY, "IP blacklist"
        
        # Check blocked ports
        dest_port = packet.get('dest_port')
        if dest_port is not None and dest_port in self.blocked_ports:
            self.stats['denied_packets'] += 1
            self._log_packet(Action.DENY, packet, "Blocked port")
            return Action.DENY, f"Port {dest_port} is blocked"
        
        # Check allowed ports (if allowed_ports is configured)
        # When allowed_ports is non-empty, it operates in allowlist mode:
        # - Packets to ports in allowed_ports are immediately allowed
        # - Packets to other ports are immediately denied
        # - Packets without dest_port bypass this check and proceed to rules
        if self.allowed_ports and dest_port is not None:
            if dest_port in self.allowed_ports:
                self.stats['allowed_packets'] += 1
                self._log_packet(Action.ALLOW, packet, "Port allowlist")
                return Action.ALLOW, f"Port {dest_port} in allowlist"
            else:
                self.stats['denied_packets'] += 1
                self._log_packet(Action.DENY, packet, "Port not in allowlist")
                return Action.DENY, f"Port {dest_port} not in allowlist"
        
        # Process through rules (in priority order)
        for rule in self.rules:
            if rule.matches(packet):
                if rule.action == Action.ALLOW:
                    self.stats['allowed_packets'] += 1
                else:
                    self.stats['denied_packets'] += 1
                self._log_packet(rule.action, packet, rule.name)
                return rule.action, f"Rule: {rule.name}"
        
        # No rules matched, use default action
        if self.default_action == Action.ALLOW:
            self.stats['allowed_packets'] += 1
        else:
            self.stats['denied_packets'] += 1
        self._log_packet(self.default_action, packet, "default policy")
        return self.default_action, "Default policy"
    
    def _log_packet(self, action: Action, packet: Dict, rule_name: str) -> None:
        """Log a packet decision"""
        log_entry = PacketLog(
            timestamp=datetime.now(),
            action=action,
            packet=packet.copy(),
            rule_name=rule_name
        )
        self.packet_logs.append(log_entry)
        
        # Log to logger
        if action == Action.DENY:
            self.logger.warning(str(log_entry))
        else:
            self.logger.debug(str(log_entry))
    
    def get_logs(self, limit: Optional[int] = None) -> List[PacketLog]:
        """
        Get packet logs.
        
        Args:
            limit: Maximum number of logs to return (most recent first)
        
        Returns:
            List of packet logs
        """
        if limit:
            return self.packet_logs[-limit:]
        return self.packet_logs.copy()
    
    def clear_logs(self) -> None:
        """Clear all packet logs"""
        self.packet_logs.clear()
        self.logger.info("Cleared packet logs")
    
    def get_stats(self) -> Dict:
        """Get firewall statistics"""
        return self.stats.copy()
    
    def reset_stats(self) -> None:
        """Reset firewall statistics"""
        for key in self.stats:
            self.stats[key] = 0
        self.logger.info("Reset statistics")
    
    def enable(self) -> None:
        """Enable the firewall"""
        self.enabled = True
        self.logger.info("Firewall enabled")
    
    def disable(self) -> None:
        """Disable the firewall"""
        self.enabled = False
        self.logger.warning("Firewall disabled")
    
    def get_rules(self) -> List[FirewallRule]:
        """Get all firewall rules"""
        return self.rules.copy()
    
    def clear_rules(self) -> None:
        """Clear all firewall rules"""
        self.rules.clear()
        self.logger.info("Cleared all rules")
