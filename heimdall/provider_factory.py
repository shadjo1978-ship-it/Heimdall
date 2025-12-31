"""
AI Provider Factory for creating provider instances.
"""
from typing import Dict, Any
from .ai_provider import AIProvider
from .openai_provider import OpenAIProvider
from .anthropic_provider import AnthropicProvider


class ProviderFactory:
    """Factory for creating AI provider instances."""
    
    @staticmethod
    def create_provider(config: Dict[str, Any]) -> AIProvider:
        """
        Create an AI provider based on configuration.
        
        Args:
            config: Provider configuration dictionary
            
        Returns:
            An instance of the appropriate AI provider
            
        Raises:
            ValueError: If provider type is not supported
        """
        provider_type = config.get('type', '').lower()
        
        if provider_type == 'openai':
            return OpenAIProvider(config)
        elif provider_type == 'anthropic':
            return AnthropicProvider(config)
        else:
            raise ValueError(f"Unsupported provider type: {provider_type}. "
                           f"Supported types: openai, anthropic")
