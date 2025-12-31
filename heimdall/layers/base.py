"""
Base layer interface for Heimdall assistant layers
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseLayer(ABC):
    """Base class for all assistant layers"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the layer with configuration
        
        Args:
            config: Layer-specific configuration dictionary
        """
        self.config = config or {}
        self.enabled = self.config.get('enabled', True)
    
    @abstractmethod
    async def process(self, input_data: Any) -> Any:
        """
        Process input through this layer
        
        Args:
            input_data: Input to process
            
        Returns:
            Processed output
        """
        pass
    
    async def initialize(self) -> None:
        """Initialize the layer (optional override)"""
        pass
    
    async def shutdown(self) -> None:
        """Cleanup layer resources (optional override)"""
        pass
