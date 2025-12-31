"""
Abstract base class for AI providers.
"""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class AIProvider(ABC):
    """Base class for all AI providers (online and local)."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the AI provider with configuration.
        
        Args:
            config: Configuration dictionary for the provider
        """
        self.config = config
        self.model = config.get('model', 'default')
        self.temperature = config.get('temperature', 0.7)
        self.max_tokens = config.get('max_tokens', 2000)
    
    @abstractmethod
    def generate_response(self, prompt: str, context: Optional[str] = None) -> str:
        """
        Generate a response from the AI model.
        
        Args:
            prompt: The user's input prompt
            context: Optional context or conversation history
            
        Returns:
            The AI-generated response as a string
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the provider is available and properly configured.
        
        Returns:
            True if the provider can be used, False otherwise
        """
        pass
