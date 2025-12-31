"""
OpenAI provider implementation for online AI.
"""
import os
from typing import Optional, Dict, Any
from .ai_provider import AIProvider


class OpenAIProvider(AIProvider):
    """OpenAI implementation for online AI services."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the OpenAI provider.
        
        Args:
            config: Configuration dictionary containing API key and model settings
        """
        super().__init__(config)
        self.api_key = config.get('api_key') or os.getenv('OPENAI_API_KEY')
        
        if not self.api_key or self.api_key == 'your-api-key-here':
            raise ValueError("OpenAI API key not configured. Set OPENAI_API_KEY environment variable.")
        
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")
    
    def generate_response(self, prompt: str, context: Optional[str] = None) -> str:
        """
        Generate a response using OpenAI's API.
        
        Args:
            prompt: The user's input prompt
            context: Optional context or conversation history
            
        Returns:
            The AI-generated response
        """
        messages = []
        
        if context:
            messages.append({"role": "system", "content": context})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def is_available(self) -> bool:
        """
        Check if OpenAI provider is available.
        
        Returns:
            True if API key is configured and valid
        """
        return bool(self.api_key and self.api_key != 'your-api-key-here')
