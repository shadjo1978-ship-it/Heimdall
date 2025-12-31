#!/usr/bin/env python3
"""
Heimdall - AI Personal Assistant
Main entry point for the Heimdall AI assistant
"""

import sys
from heimdall_persona import HeimdallPersona


class Heimdall:
    """Main Heimdall AI Assistant class"""
    
    def __init__(self):
        self.persona = HeimdallPersona()
        self.conversation_history = []
        
    def process_query(self, query):
        """
        Process a user query and return a response
        """
        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": query})
        
        # Simulate thinking process
        thinking = self._generate_thinking(query)
        
        # Generate response
        response = self._generate_response(query)
        
        # Format with persona
        formatted_response = self.persona.format_response(thinking, response, query)
        
        # Add to conversation history
        self.conversation_history.append({"role": "assistant", "content": response})
        
        return formatted_response
    
    def _generate_thinking(self, query):
        """Generate thinking process for the query"""
        return f"""Let me analyze this query...
Query: "{query}"

1. Understanding the request
2. Checking for security implications
3. Formulating a helpful response
4. Ensuring safety and accuracy"""
    
    def _generate_response(self, query):
        """Generate a response to the query"""
        # This is a basic implementation - in a real system, this would integrate with an LLM
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["hello", "hi", "hey"]):
            return """Greetings! I am Heimdall, your AI guardian assistant. 

I'm here to help you with various tasks while keeping you safe and secure. I can:
- Answer questions and provide information
- Assist with tasks and problem-solving
- Alert you to potential security concerns
- Show you my thinking process in real-time

How may I assist you today?"""
        
        elif any(word in query_lower for word in ["who are you", "what are you"]):
            return f"""I am {self.persona.name}, named after the all-seeing guardian of Norse mythology.

As your AI personal assistant, I combine:
- Real-time thinking: I show you how I process and reason through requests
- Voice-ready interaction: I communicate naturally and conversationally  
- Firewall protection: I watch for security risks and warn you of potential threats
- Personal assistance: I help with a wide range of tasks and questions

Like Heimdall guarding the Bifrost bridge, I stand watch at the gateway between you and the digital realm, ensuring your safety while helping you accomplish your goals."""
        
        elif "help" in query_lower or "capabilities" in query_lower:
            capabilities = "\n".join([f"  • {cap}" for cap in self.persona.capabilities])
            return f"""I'm designed to assist you with vigilance and wisdom. My capabilities include:

{capabilities}

I prioritize your safety and security in all interactions. Feel free to ask me anything, and I'll do my best to help while keeping you informed of any potential concerns."""
        
        else:
            return f"""I've received your query: "{query}"

In a full implementation, I would process this using advanced AI capabilities. For now, I'm demonstrating the Heimdall persona framework, which includes:

- Security assessment of requests
- Real-time thinking display
- Protective guidance
- Helpful responses

This framework can be integrated with any LLM API (OpenAI, Anthropic, etc.) to provide fully functional AI assistance."""
    
    def interactive_mode(self):
        """Run Heimdall in interactive mode"""
        print("\n" + "=" * 70)
        print(f"  {self.persona.name} - {self.persona.role}")
        print("  Type 'exit' or 'quit' to end the session")
        print("=" * 70 + "\n")
        
        while True:
            try:
                user_input = input("\n💬 You: ").strip()
                
                if not user_input:
                    continue
                    
                if user_input.lower() in ["exit", "quit", "bye"]:
                    print("\n🛡️ Heimdall: Farewell! Stay safe and secure.")
                    break
                
                response = self.process_query(user_input)
                print(f"\n{response}\n")
                
            except KeyboardInterrupt:
                print("\n\n🛡️ Heimdall: Session interrupted. Stay safe!")
                break
            except EOFError:
                break


def main():
    """Main entry point"""
    heimdall = Heimdall()
    
    if len(sys.argv) > 1:
        # Process command line argument as query
        query = " ".join(sys.argv[1:])
        response = heimdall.process_query(query)
        print(response)
    else:
        # Run in interactive mode
        heimdall.interactive_mode()


if __name__ == "__main__":
    main()
