"""
Main Heimdall AI Assistant application.
"""
from typing import Optional
from .config import load_config
from .provider_factory import ProviderFactory
from .ai_provider import AIProvider


class Heimdall:
    """Main Heimdall AI Assistant class."""
    
    def __init__(self, config_path: str = 'config.yaml'):
        """
        Initialize Heimdall with configuration.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = load_config(config_path)
        self.ai_provider: Optional[AIProvider] = None
        self._initialize_ai_provider()
        
    def _initialize_ai_provider(self):
        """Initialize the AI provider from configuration."""
        ai_config = self.config.get('ai_provider', {})
        try:
            self.ai_provider = ProviderFactory.create_provider(ai_config)
            if not self.ai_provider.is_available():
                print("Warning: AI provider is not properly configured.")
        except Exception as e:
            print(f"Error initializing AI provider: {e}")
            self.ai_provider = None
    
    def ask(self, prompt: str, context: Optional[str] = None) -> str:
        """
        Ask Heimdall a question and get a response.
        
        Args:
            prompt: The user's question or prompt
            context: Optional context for the conversation
            
        Returns:
            The AI-generated response
        """
        if not self.ai_provider:
            return "AI provider not initialized. Please check your configuration."
        
        # Apply firewall/content filtering if enabled
        if self.config.get('firewall', {}).get('enabled', True):
            filtered_prompt = self._apply_content_filter(prompt)
        else:
            filtered_prompt = prompt
        
        # Generate response using online AI
        response = self.ai_provider.generate_response(filtered_prompt, context)
        
        return response
    
    def _apply_content_filter(self, text: str) -> str:
        """
        Apply content filtering based on firewall settings.
        
        Args:
            text: The text to filter
            
        Returns:
            Filtered text
        """
        blocked_keywords = self.config.get('firewall', {}).get('blocked_keywords', [])
        
        # Simple keyword blocking
        for keyword in blocked_keywords:
            if keyword.lower() in text.lower():
                return f"[Content blocked: contains restricted keyword '{keyword}']"
        
        return text
