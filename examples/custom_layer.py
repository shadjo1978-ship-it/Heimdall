"""
Custom layer example - showing how to extend Heimdall
"""

import asyncio
from typing import Any, Dict, Optional
from heimdall import Assistant
from heimdall.layers.base import BaseLayer
from heimdall.utils import get_default_config


class CustomLoggingLayer(BaseLayer):
    """Example custom layer for logging"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.log_level = self.config.get('log_level', 'INFO')
    
    async def process(self, input_data: Any) -> Any:
        """Log the input and pass it through"""
        print(f"[{self.log_level}] Processing: {str(input_data)[:100]}")
        return input_data


async def main():
    """Demonstrate custom layer usage"""
    
    print("Custom Layer Example")
    print("=" * 50)
    
    # Create assistant
    config = get_default_config()
    assistant = Assistant(config)
    
    # Add custom layer
    custom_layer = CustomLoggingLayer({'log_level': 'DEBUG'})
    assistant.layers.insert(0, custom_layer)  # Add at the beginning
    
    await assistant.initialize()
    
    # Use the assistant
    message = "Testing custom layer"
    response = await assistant.chat(message)
    print(f"\nResponse: {response}")
    
    await assistant.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
