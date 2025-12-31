"""
Firewall configuration management
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional
from firewall_engine import FirewallEngine, FirewallRule, Action, Protocol


class FirewallConfig:
    """Manages firewall configuration loading and saving"""
    
    @staticmethod
    def load_from_json(filepath: str, engine: FirewallEngine) -> None:
        """
        Load firewall configuration from a JSON file.
        
        Args:
            filepath: Path to the JSON configuration file
            engine: FirewallEngine instance to configure
        """
        with open(filepath, 'r') as f:
            config = json.load(f)
        
        FirewallConfig._apply_config(config, engine)
    
    @staticmethod
    def load_from_yaml(filepath: str, engine: FirewallEngine) -> None:
        """
        Load firewall configuration from a YAML file.
        
        Args:
            filepath: Path to the YAML configuration file
            engine: FirewallEngine instance to configure
        """
        with open(filepath, 'r') as f:
            config = yaml.safe_load(f)
        
        FirewallConfig._apply_config(config, engine)
    
    @staticmethod
    def _apply_config(config: Dict, engine: FirewallEngine) -> None:
        """Apply configuration to the firewall engine"""
        
        # Set default action
        if 'default_action' in config:
            engine.default_action = Action(config['default_action'].lower())
        
        # Load rules
        if 'rules' in config:
            for rule_config in config['rules']:
                rule = FirewallRule(
                    name=rule_config['name'],
                    action=Action(rule_config['action'].lower()),
                    protocol=Protocol(rule_config.get('protocol', 'any').lower()),
                    source_ip=rule_config.get('source_ip'),
                    dest_ip=rule_config.get('dest_ip'),
                    source_port=rule_config.get('source_port'),
                    dest_port=rule_config.get('dest_port'),
                    priority=rule_config.get('priority', 100),
                    enabled=rule_config.get('enabled', True)
                )
                engine.add_rule(rule)
        
        # Load blacklist
        if 'blacklist' in config:
            for ip in config['blacklist']:
                engine.add_to_blacklist(ip)
        
        # Load whitelist
        if 'whitelist' in config:
            for ip in config['whitelist']:
                engine.add_to_whitelist(ip)
        
        # Load blocked ports
        if 'blocked_ports' in config:
            for port in config['blocked_ports']:
                engine.block_port(port)
        
        # Load allowed ports
        if 'allowed_ports' in config:
            for port in config['allowed_ports']:
                engine.allow_port(port)
    
    @staticmethod
    def save_to_json(filepath: str, engine: FirewallEngine) -> None:
        """
        Save firewall configuration to a JSON file.
        
        Args:
            filepath: Path to save the JSON configuration
            engine: FirewallEngine instance to save
        """
        config = FirewallConfig._export_config(engine)
        
        with open(filepath, 'w') as f:
            json.dump(config, f, indent=2)
    
    @staticmethod
    def save_to_yaml(filepath: str, engine: FirewallEngine) -> None:
        """
        Save firewall configuration to a YAML file.
        
        Args:
            filepath: Path to save the YAML configuration
            engine: FirewallEngine instance to save
        """
        config = FirewallConfig._export_config(engine)
        
        with open(filepath, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
    
    @staticmethod
    def _export_config(engine: FirewallEngine) -> Dict:
        """Export engine configuration to a dictionary"""
        config = {
            'default_action': engine.default_action.value,
            'rules': [],
            'blacklist': list(engine.blacklist_ips),
            'whitelist': list(engine.whitelist_ips),
            'blocked_ports': list(engine.blocked_ports),
            'allowed_ports': list(engine.allowed_ports)
        }
        
        # Export rules
        for rule in engine.rules:
            rule_config = {
                'name': rule.name,
                'action': rule.action.value,
                'protocol': rule.protocol.value,
                'priority': rule.priority,
                'enabled': rule.enabled
            }
            
            if rule.source_ip:
                rule_config['source_ip'] = rule.source_ip
            if rule.dest_ip:
                rule_config['dest_ip'] = rule.dest_ip
            if rule.source_port is not None:
                rule_config['source_port'] = rule.source_port
            if rule.dest_port is not None:
                rule_config['dest_port'] = rule.dest_port
            
            config['rules'].append(rule_config)
        
        return config
