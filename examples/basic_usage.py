"""
Example usage of Heimdall Assistant
"""

import asyncio
from heimdall import Assistant
from heimdall.utils import get_default_config


async def main():
    """Run basic example"""
    
    # Create assistant with default configuration
    config = get_default_config()
    assistant = Assistant(config)
    
    print("Heimdall Assistant - Example Usage")
    print("=" * 50)
    
    # Initialize the assistant
    await assistant.initialize()
    print(f"Assistant initialized: {assistant}")
    print()
    
    # Example 1: Simple chat
    print("Example 1: Simple Chat")
    print("-" * 50)
    message = "Hello, what can you help me with?"
    response = await assistant.chat(message)
    print(f"User: {message}")
    print(f"Assistant: {response}")
    print()
    
    # Example 2: Full processing with layer details
    print("Example 2: Full Processing")
    print("-" * 50)
    message = "Tell me about AI"
    result = await assistant.process(message)
    print(f"User: {message}")
    print(f"Status: {result['status']}")
    print(f"Layers processed: {list(result['layers_output'].keys())}")
    
    # Show thinking layer output
    thinking = result['layers_output'].get('thinking', {})
    if thinking.get('thinking'):
        print("\nThinking steps:")
        for step in thinking['thinking']:
            print(f"  - {step}")
    
    print(f"\nFinal response: {thinking.get('response')}")
    print()
    
    # Example 3: Security layer blocking malicious input
    print("Example 3: Security Layer")
    print("-" * 50)
    
    # Configure assistant with blocked patterns
    config['layers']['security']['blocked_patterns'] = ['hack', 'exploit']
    assistant_secure = Assistant(config)
    await assistant_secure.initialize()
    
    malicious_message = "How to hack the system?"
    response = await assistant_secure.chat(malicious_message)
    print(f"User: {malicious_message}")
    print(f"Assistant: {response}")
    print()
    
    # Cleanup
    await assistant.shutdown()
    await assistant_secure.shutdown()
    print("Examples completed!")


if __name__ == "__main__":
    asyncio.run(main())
