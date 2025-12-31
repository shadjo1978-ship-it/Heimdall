"""
Anthropic provider implementation for online AI.
"""
import os
from typing import Optional, Dict, Any
from .ai_provider import AIProvider


class AnthropicProvider(AIProvider):
    """Anthropic Claude implementation for online AI services."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Anthropic provider.
        
        Args:
            config: Configuration dictionary containing API key and model settings
        """
        super().__init__(config)
        self.api_key = config.get('api_key') or os.getenv('ANTHROPIC_API_KEY')
        
        if not self.api_key or self.api_key == 'your-api-key-here':
            raise ValueError("Anthropic API key not configured. Set ANTHROPIC_API_KEY environment variable.")
        
        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=self.api_key)
        except ImportError:
            raise ImportError("anthropic package not installed. Run: pip install anthropic")
    
    def generate_response(self, prompt: str, context: Optional[str] = None) -> str:
        """
        Generate a response using Anthropic's API.
        
        Args:
            prompt: The user's input prompt
            context: Optional context or conversation history
            
        Returns:
            The AI-generated response
        """
        system_message = context if context else "You are Heimdall, an AI personal assistant."
        
        try:
            response = self.client.messages.create(
                model=self.model or "claude-3-opus-20240229",
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=system_message,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def is_available(self) -> bool:
        """
        Check if Anthropic provider is available.
        
        Returns:
            True if API key is configured and valid
        """
        return bool(self.api_key and self.api_key != 'your-api-key-here')
