"""
Configuration utilities for Heimdall
"""

import os
import yaml
from typing import Dict, Any


def load_config(config_path: str = None) -> Dict[str, Any]:
    """
    Load configuration from YAML file
    
    Args:
        config_path: Path to config file, defaults to config.yml
        
    Returns:
        Configuration dictionary
    """
    if config_path is None:
        config_path = os.path.join(os.getcwd(), 'config.yml')
    
    if not os.path.exists(config_path):
        return get_default_config()
    
    with open(config_path, 'r') as f:
        return yaml.safe_load(f) or {}


def get_default_config() -> Dict[str, Any]:
    """
    Get default configuration
    
    Returns:
        Default configuration dictionary
    """
    return {
        'layers': {
            'security': {
                'enabled': True,
                'blocked_patterns': [],
                'rate_limit': 100,
                'sanitize_input': True
            },
            'voice': {
                'enabled': True,
                'sample_rate': 16000,
                'language': 'en-US'
            },
            'thinking': {
                'enabled': True,
                'model': 'default',
                'temperature': 0.7,
                'real_time': True
            }
        }
    }


def save_config(config: Dict[str, Any], config_path: str = None) -> None:
    """
    Save configuration to YAML file
    
    Args:
        config: Configuration dictionary
        config_path: Path to save config file
    """
    if config_path is None:
        config_path = os.path.join(os.getcwd(), 'config.yml')
    
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
