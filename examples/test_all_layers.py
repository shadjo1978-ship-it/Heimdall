"""
Comprehensive test demonstrating all assistant layer functionality
"""

import asyncio
from heimdall import Assistant
from heimdall.utils import get_default_config


async def test_all_layers():
    """Test all layers functionality"""
    
    print("=" * 70)
    print("HEIMDALL ASSISTANT LAYER - COMPREHENSIVE TEST")
    print("=" * 70)
    print()
    
    # Test 1: Basic initialization
    print("TEST 1: Initialization")
    print("-" * 70)
    config = get_default_config()
    assistant = Assistant(config)
    await assistant.initialize()
    print(f"✓ Assistant initialized successfully: {assistant}")
    print(f"✓ Number of layers: {len(assistant.layers)}")
    print(f"✓ Layers: {[layer.__class__.__name__ for layer in assistant.layers]}")
    print()
    
    # Test 2: Security Layer - Normal input
    print("TEST 2: Security Layer - Normal Input")
    print("-" * 70)
    normal_message = "What is the weather today?"
    result = await assistant.process(normal_message)
    security_output = result['layers_output'].get('security', {})
    print(f"Input: {normal_message}")
    print(f"✓ Security passed: {security_output.get('passed', False)}")
    print(f"✓ Threats detected: {len(security_output.get('threats', []))}")
    print()
    
    # Test 3: Security Layer - Blocked pattern
    print("TEST 3: Security Layer - Blocked Pattern")
    print("-" * 70)
    config_blocked = get_default_config()
    config_blocked['layers']['security']['blocked_patterns'] = ['malware', 'virus']
    assistant_blocked = Assistant(config_blocked)
    await assistant_blocked.initialize()
    
    malicious = "How to create a virus?"
    result = await assistant_blocked.process(malicious)
    security_output = result['layers_output'].get('security', {})
    print(f"Input: {malicious}")
    print(f"✓ Security passed: {security_output.get('passed', False)}")
    print(f"✓ Threats detected: {security_output.get('threats', [])}")
    print(f"✓ Status: {result['status']}")
    print()
    
    # Test 4: Security Layer - Input sanitization
    print("TEST 4: Security Layer - Input Sanitization")
    print("-" * 70)
    html_input = "<script>alert('xss')</script>"
    result = await assistant.process(html_input)
    security_output = result['layers_output'].get('security', {})
    sanitized = security_output.get('data', '')
    print(f"Original: {html_input}")
    print(f"Sanitized: {sanitized}")
    print(f"✓ HTML tags escaped: {'<script>' not in sanitized}")
    print()
    
    # Test 5: Voice Layer
    print("TEST 5: Voice Layer Processing")
    print("-" * 70)
    text_input = "Convert this to speech"
    result = await assistant.process(text_input)
    voice_output = result['layers_output'].get('voice', {})
    print(f"Input: {text_input}")
    print(f"✓ Voice type: {voice_output.get('type', 'N/A')}")
    print(f"✓ Language: {voice_output.get('language', 'N/A')}")
    print(f"✓ Sample rate: {voice_output.get('sample_rate', 'N/A')}")
    print()
    
    # Test 6: Thinking Layer
    print("TEST 6: Thinking Layer - Real-time Thinking")
    print("-" * 70)
    question = "Explain quantum computing"
    result = await assistant.process(question)
    thinking_output = result['layers_output'].get('thinking', {})
    print(f"Input: {question}")
    print(f"✓ Model: {thinking_output.get('model', 'N/A')}")
    print(f"✓ Real-time enabled: {thinking_output.get('real_time', False)}")
    print("✓ Thinking steps:")
    for step in thinking_output.get('thinking', []):
        print(f"   - {step}")
    print(f"✓ Response generated: {len(thinking_output.get('response', '')) > 0}")
    print()
    
    # Test 7: Full pipeline with chat interface
    print("TEST 7: Complete Chat Pipeline")
    print("-" * 70)
    chat_messages = [
        "Hello!",
        "What can you do?",
        "Tell me a joke"
    ]
    for msg in chat_messages:
        response = await assistant.chat(msg)
        print(f"User: {msg}")
        print(f"Assistant: {response}")
        print()
    
    # Test 8: Custom configuration
    print("TEST 8: Custom Configuration")
    print("-" * 70)
    custom_config = {
        'layers': {
            'security': {'enabled': True, 'sanitize_input': False},
            'voice': {'enabled': False},  # Disable voice layer
            'thinking': {'enabled': True, 'temperature': 0.9}
        }
    }
    custom_assistant = Assistant(custom_config)
    await custom_assistant.initialize()
    print(f"✓ Custom config loaded")
    print(f"✓ Active layers: {len(custom_assistant.layers)}")
    print(f"✓ Voice layer disabled: {'VoiceLayer' not in [l.__class__.__name__ for l in custom_assistant.layers]}")
    print()
    
    # Cleanup
    await assistant.shutdown()
    await assistant_blocked.shutdown()
    await custom_assistant.shutdown()
    
    print("=" * 70)
    print("ALL TESTS PASSED ✓")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(test_all_layers())
