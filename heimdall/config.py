"""
Configuration loader for Heimdall.
"""
import os
import yaml
from typing import Dict, Any
from dotenv import load_dotenv


def load_config(config_path: str = 'config.yaml') -> Dict[str, Any]:
    """
    Load configuration from YAML file and environment variables.
    
    Args:
        config_path: Path to the configuration YAML file
        
    Returns:
        Configuration dictionary
    """
    # Load environment variables from .env file if it exists
    load_dotenv()
    
    # Load YAML configuration
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Override API key from environment if available
    if 'ai_provider' in config:
        env_api_key = os.getenv('HEIMDALL_API_KEY')
        if env_api_key:
            config['ai_provider']['api_key'] = env_api_key
    
    return config
