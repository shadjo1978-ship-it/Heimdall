#!/usr/bin/env python3
"""
Heimdall - AI Personal Assistant with Text and Voice
A starter program for an AI assistant that supports both text and voice interactions.
"""

import os
import sys
import json
from pathlib import Path

# Try importing optional dependencies
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    print("Warning: speech_recognition not available. Voice input will be disabled.")

try:
    import pyttsx3
    TEXT_TO_SPEECH_AVAILABLE = True
except ImportError:
    TEXT_TO_SPEECH_AVAILABLE = False
    print("Warning: pyttsx3 not available. Voice output will be disabled.")


class Heimdall:
    """Main Heimdall AI Assistant class."""
    
    def __init__(self, config_file="config.json"):
        """Initialize Heimdall assistant."""
        self.config = self.load_config(config_file)
        self.voice_enabled = self.config.get("voice_enabled", False)
        
        # Initialize speech recognition
        if SPEECH_RECOGNITION_AVAILABLE and self.voice_enabled:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
        else:
            self.recognizer = None
            self.microphone = None
        
        # Initialize text-to-speech
        if TEXT_TO_SPEECH_AVAILABLE and self.voice_enabled:
            self.tts_engine = pyttsx3.init()
            # Configure voice properties
            self.tts_engine.setProperty('rate', self.config.get('speech_rate', 150))
            self.tts_engine.setProperty('volume', self.config.get('speech_volume', 0.9))
        else:
            self.tts_engine = None
        
        print("Heimdall AI Assistant initialized.")
        if self.voice_enabled:
            print("Voice features enabled.")
    
    def load_config(self, config_file):
        """Load configuration from JSON file."""
        config_path = Path(config_file)
        if config_path.exists():
            with open(config_path, 'r') as f:
                return json.load(f)
        else:
            # Return default configuration
            return {
                "voice_enabled": False,
                "speech_rate": 150,
                "speech_volume": 0.9,
                "assistant_name": "Heimdall"
            }
    
    def speak(self, text):
        """Convert text to speech."""
        print(f"Heimdall: {text}")
        if self.tts_engine and self.voice_enabled:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
    
    def listen(self):
        """Listen for voice input and convert to text."""
        if not self.recognizer or not self.microphone:
            return None
        
        try:
            with self.microphone as source:
                print("Listening...")
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5)
            
            print("Processing speech...")
            # Use Google Speech Recognition
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.WaitTimeoutError:
            print("No speech detected.")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio.")
            return None
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
            return None
    
    def process_command(self, command):
        """Process user command and generate response."""
        command_lower = command.lower().strip()
        
        # Basic commands
        if command_lower in ["hello", "hi", "hey"]:
            return "Hello! I'm Heimdall, your AI assistant. How can I help you today?"
        
        elif command_lower in ["how are you", "how are you?"]:
            return "I'm functioning optimally. Thank you for asking! How can I assist you?"
        
        elif "your name" in command_lower:
            return f"I am {self.config.get('assistant_name', 'Heimdall')}, your AI personal assistant."
        
        elif "help" in command_lower:
            return self.get_help_message()
        
        elif command_lower in ["quit", "exit", "bye", "goodbye"]:
            return None  # Signal to exit
        
        elif "voice on" in command_lower or "enable voice" in command_lower:
            if TEXT_TO_SPEECH_AVAILABLE and SPEECH_RECOGNITION_AVAILABLE:
                self.voice_enabled = True
                return "Voice features enabled."
            else:
                return "Voice features are not available. Please install required dependencies."
        
        elif "voice off" in command_lower or "disable voice" in command_lower:
            self.voice_enabled = False
            return "Voice features disabled."
        
        else:
            # Default response for unknown commands
            return f"You said: '{command}'. I'm still learning. Try saying 'help' for available commands."
    
    def get_help_message(self):
        """Return help message with available commands."""
        help_text = """
Available Commands:
- hello/hi/hey: Greet Heimdall
- help: Show this help message
- your name: Ask for assistant's name
- how are you: Check assistant status
- voice on/off: Enable or disable voice features
- quit/exit/bye: Exit the program

You can interact using text input or voice (if enabled).
        """
        return help_text.strip()
    
    def run(self):
        """Main interaction loop."""
        self.speak(f"Welcome! I'm {self.config.get('assistant_name', 'Heimdall')}.")
        self.speak("Type 'help' for available commands or 'quit' to exit.")
        
        while True:
            try:
                # Get input (text or voice)
                if self.voice_enabled and self.recognizer and self.microphone:
                    print("\n[Press Enter for voice input, or type your message]")
                    user_input = input("You: ").strip()
                    
                    if not user_input:
                        # Voice input mode
                        user_input = self.listen()
                        if not user_input:
                            continue
                else:
                    user_input = input("\nYou: ").strip()
                
                if not user_input:
                    continue
                
                # Process command
                response = self.process_command(user_input)
                
                if response is None:
                    # Exit signal
                    self.speak("Goodbye! Stay safe.")
                    break
                
                # Output response
                self.speak(response)
                
            except KeyboardInterrupt:
                print("\n")
                self.speak("Interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
                continue


def main():
    """Main entry point."""
    print("=" * 50)
    print("HEIMDALL - AI Personal Assistant")
    print("Text and Voice Interaction")
    print("=" * 50)
    print()
    
    # Create and run assistant
    assistant = Heimdall()
    assistant.run()


if __name__ == "__main__":
    main()
