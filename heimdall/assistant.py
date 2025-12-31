"""
Main Assistant orchestrator that coordinates all layers
"""

import asyncio
from typing import Any, Dict, List, Optional
from heimdall.layers import VoiceLayer, ThinkingLayer, SecurityLayer, BaseLayer


class Assistant:
    """
    Main Heimdall Assistant class that orchestrates all layers
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the assistant with configuration
        
        Args:
            config: Configuration dictionary for the assistant
        """
        self.config = config or {}
        self.layers: List[BaseLayer] = []
        self._initialized = False
        
        # Initialize layers
        self._setup_layers()
    
    def _setup_layers(self) -> None:
        """Setup all assistant layers"""
        layers_config = self.config.get('layers', {})
        
        # Security layer (first for input validation)
        if layers_config.get('security', {}).get('enabled', True):
            self.layers.append(SecurityLayer(layers_config.get('security', {})))
        
        # Voice layer
        if layers_config.get('voice', {}).get('enabled', True):
            self.layers.append(VoiceLayer(layers_config.get('voice', {})))
        
        # Thinking layer (core AI processing)
        if layers_config.get('thinking', {}).get('enabled', True):
            self.layers.append(ThinkingLayer(layers_config.get('thinking', {})))
    
    async def initialize(self) -> None:
        """Initialize all layers"""
        if self._initialized:
            return
        
        for layer in self.layers:
            await layer.initialize()
        
        self._initialized = True
    
    async def shutdown(self) -> None:
        """Shutdown all layers"""
        for layer in self.layers:
            await layer.shutdown()
        
        self._initialized = False
    
    async def process(self, input_data: Any) -> Dict[str, Any]:
        """
        Process input through all layers
        
        Args:
            input_data: Input to process (text, voice, etc.)
            
        Returns:
            Processed response from the assistant
        """
        if not self._initialized:
            await self.initialize()
        
        result = {
            'input': input_data,
            'layers_output': {},
            'final_response': None,
            'status': 'success'
        }
        
        # Process through security layer first
        security_result = None
        for layer in self.layers:
            if isinstance(layer, SecurityLayer):
                security_result = await layer.process(input_data)
                result['layers_output']['security'] = security_result
                
                if not security_result.get('passed', True):
                    result['status'] = 'blocked'
                    result['final_response'] = {
                        'error': 'Security check failed',
                        'threats': security_result.get('threats', [])
                    }
                    return result
                
                # Use sanitized data for further processing
                input_data = security_result.get('data', input_data)
                break
        
        # Process through other layers
        current_data = input_data
        for layer in self.layers:
            if isinstance(layer, SecurityLayer):
                continue  # Already processed
            
            layer_output = await layer.process(current_data)
            layer_name = layer.__class__.__name__.replace('Layer', '').lower()
            result['layers_output'][layer_name] = layer_output
            current_data = layer_output
        
        result['final_response'] = current_data
        return result
    
    async def chat(self, message: str) -> str:
        """
        Simple chat interface
        
        Args:
            message: User message
            
        Returns:
            Assistant response
        """
        result = await self.process(message)
        
        if result['status'] == 'blocked':
            return f"Security: {result['final_response']['error']}"
        
        # Extract response from thinking layer
        thinking_output = result['layers_output'].get('thinking', {})
        return thinking_output.get('response', 'No response generated')
    
    def __repr__(self) -> str:
        return f"<Assistant layers={len(self.layers)} initialized={self._initialized}>"
