#!/usr/bin/env python3
"""
Heimdall - AI Personal Assistant with Online AI Support

This is the main entry point for running Heimdall.
"""
import sys
import argparse
from heimdall.heimdall import Heimdall


def main():
    """Main entry point for Heimdall CLI."""
    parser = argparse.ArgumentParser(
        description='Heimdall - AI Personal Assistant with real-time thinking'
    )
    parser.add_argument(
        '--config',
        default='config.yaml',
        help='Path to configuration file (default: config.yaml)'
    )
    parser.add_argument(
        '--prompt',
        help='Single prompt to send to Heimdall'
    )
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Run in interactive mode'
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize Heimdall
        heimdall = Heimdall(config_path=args.config)
        
        if args.prompt:
            # Single prompt mode
            response = heimdall.ask(args.prompt)
            print(f"\nHeimdall: {response}\n")
        elif args.interactive:
            # Interactive mode
            print("Heimdall AI Assistant - Interactive Mode")
            print("Type 'exit' or 'quit' to end the session.\n")
            
            context = "You are Heimdall, an AI personal assistant with real-time thinking capabilities."
            
            while True:
                try:
                    user_input = input("You: ").strip()
                    
                    if user_input.lower() in ['exit', 'quit']:
                        print("Goodbye!")
                        break
                    
                    if not user_input:
                        continue
                    
                    response = heimdall.ask(user_input, context=context)
                    print(f"Heimdall: {response}\n")
                    
                except KeyboardInterrupt:
                    print("\nGoodbye!")
                    break
        else:
            # No mode specified, show help
            parser.print_help()
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
