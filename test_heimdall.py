#!/usr/bin/env python3
"""
Test suite for Heimdall AI Persona
Validates core functionality of the persona and security features
"""

import sys
from heimdall_persona import HeimdallPersona
from heimdall import Heimdall


def test_persona_initialization():
    """Test that the persona initializes correctly"""
    print("Testing persona initialization...")
    persona = HeimdallPersona()
    
    assert persona.name == "Heimdall"
    assert persona.role == "AI Guardian Assistant"
    assert len(persona.capabilities) == 4
    assert "real-time thinking" in persona.capabilities
    assert "firewall protection" in persona.capabilities
    
    print("✅ Persona initialization test passed")


def test_system_prompt():
    """Test that system prompt is generated"""
    print("\nTesting system prompt generation...")
    persona = HeimdallPersona()
    prompt = persona.get_system_prompt()
    
    assert "Heimdall" in prompt
    assert "guardian" in prompt
    assert "security" in prompt
    assert len(prompt) > 100
    
    print("✅ System prompt generation test passed")


def test_security_assessment():
    """Test security risk assessment"""
    print("\nTesting security risk assessment...")
    persona = HeimdallPersona()
    
    # Test high risk
    risk, warning = persona.assess_security_risk("I need my password reset")
    assert risk == "high"
    assert "password" in warning.lower()
    
    # Test medium risk
    risk, warning = persona.assess_security_risk("Can you help me download this?")
    assert risk == "medium"
    assert "download" in warning.lower()
    
    # Test low risk
    risk, warning = persona.assess_security_risk("Can you open this link?")
    assert risk == "low"
    
    # Test no risk
    risk, warning = persona.assess_security_risk("What's the weather?")
    assert risk == "none"
    assert warning == ""
    
    print("✅ Security assessment test passed")


def test_response_formatting():
    """Test response formatting with thinking"""
    print("\nTesting response formatting...")
    persona = HeimdallPersona()
    
    thinking = "Analyzing the query..."
    response = "Here is my response"
    query = "Test query"
    
    formatted = persona.format_response(thinking, response, query)
    
    assert "🧠" in formatted
    assert "🛡️" in formatted
    assert thinking in formatted
    assert response in formatted
    
    print("✅ Response formatting test passed")


def test_heimdall_query_processing():
    """Test Heimdall query processing"""
    print("\nTesting Heimdall query processing...")
    heimdall = Heimdall()
    
    # Test greeting
    response = heimdall.process_query("Hello")
    assert "Greetings" in response or "greeting" in response.lower()
    
    # Test who are you
    response = heimdall.process_query("Who are you?")
    assert "Heimdall" in response
    
    # Test capabilities
    response = heimdall.process_query("What can you help with?")
    assert len(response) > 0
    
    print("✅ Heimdall query processing test passed")


def test_conversation_history():
    """Test that conversation history is maintained"""
    print("\nTesting conversation history...")
    heimdall = Heimdall()
    
    assert len(heimdall.conversation_history) == 0
    
    heimdall.process_query("Hello")
    assert len(heimdall.conversation_history) == 2  # User + assistant
    
    heimdall.process_query("How are you?")
    assert len(heimdall.conversation_history) == 4
    
    print("✅ Conversation history test passed")


def run_all_tests():
    """Run all tests"""
    print("=" * 70)
    print("  Heimdall AI Persona Test Suite")
    print("=" * 70)
    
    try:
        test_persona_initialization()
        test_system_prompt()
        test_security_assessment()
        test_response_formatting()
        test_heimdall_query_processing()
        test_conversation_history()
        
        print("\n" + "=" * 70)
        print("  ✅ All tests passed!")
        print("=" * 70)
        return 0
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
