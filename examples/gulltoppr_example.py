#!/usr/bin/env python3
"""
Example script demonstrating Gulltoppr integration with Heimdall.

This script shows how to:
1. Connect to the Gulltoppr service
2. Analyze smart contracts
3. Generate ABIs
4. Handle responses
"""

import json
import requests
import sys
from typing import Dict, Optional


class GulltopprClient:
    """Client for interacting with the Gulltoppr service."""
    
    def __init__(self, config_path: str = "gulltoppr-config.json"):
        """Initialize the Gulltoppr client with configuration."""
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        self.config = config['gulltoppr']
        self.service_url = self.config['service_url']
        self.default_rpc_url = self.config['default_rpc_url']
        self.timeout = self.config['timeout'] / 1000  # Convert to seconds
        
        if not self.config['enabled']:
            raise Exception("Gulltoppr integration is disabled in configuration")
    
    def health_check(self) -> bool:
        """Check if Gulltoppr service is running."""
        try:
            response = requests.get(
                self.service_url,
                timeout=self.timeout
            )
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"Health check failed: {e}")
            return False
    
    def generate_abi(
        self, 
        contract_address: str, 
        rpc_url: Optional[str] = None
    ) -> Dict:
        """
        Generate ABI for a smart contract.
        
        Args:
            contract_address: Ethereum contract address (0x...)
            rpc_url: RPC endpoint URL (optional, uses default if not provided)
        
        Returns:
            Dictionary containing ABI and analysis results
        """
        if not contract_address.startswith('0x'):
            raise ValueError("Contract address must start with '0x'")
        
        rpc = rpc_url or self.default_rpc_url
        url = f"{self.service_url}/{contract_address}"
        
        try:
            response = requests.get(
                url,
                params={'rpc_url': rpc},
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error generating ABI: {e}")
            raise
    
    def analyze_contract(
        self, 
        contract_address: str, 
        rpc_url: Optional[str] = None
    ) -> None:
        """
        Analyze a smart contract and print results.
        
        Args:
            contract_address: Ethereum contract address
            rpc_url: RPC endpoint URL (optional)
        """
        print(f"Analyzing contract: {contract_address}")
        print("-" * 60)
        
        try:
            result = self.generate_abi(contract_address, rpc_url)
            
            print("✓ Analysis complete!")
            print(f"Contract: {contract_address}")
            
            if 'abi' in result:
                print(f"ABI generated with {len(result['abi'])} functions")
                print("\nABI Preview:")
                print(json.dumps(result['abi'][:3], indent=2))  # Show first 3 functions
                if len(result['abi']) > 3:
                    print(f"... and {len(result['abi']) - 3} more functions")
            
            print("\nFull result saved to: contract_analysis.json")
            with open('contract_analysis.json', 'w') as f:
                json.dump(result, f, indent=2)
                
        except Exception as e:
            print(f"✗ Analysis failed: {e}")
            raise


def main():
    """Main function demonstrating Gulltoppr usage."""
    
    # Example contract addresses (well-known contracts)
    examples = {
        "USDT": "0xdac17f958d2ee523a2206206994597c13d831ec7",
        "USDC": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
        "DAI": "0x6b175474e89094c44da98b954eedeac495271d0f"
    }
    
    print("=" * 60)
    print("Gulltoppr Integration Example")
    print("=" * 60)
    print()
    
    try:
        # Initialize client
        client = GulltopprClient()
        
        # Health check
        print("Checking Gulltoppr service...")
        if client.health_check():
            print("✓ Gulltoppr service is running\n")
        else:
            print("✗ Gulltoppr service is not available")
            print("Please ensure Gulltoppr is running:")
            print("  docker-compose up -d")
            sys.exit(1)
        
        # Get contract address from command line or use example
        if len(sys.argv) > 1:
            contract_address = sys.argv[1]
            rpc_url = sys.argv[2] if len(sys.argv) > 2 else None
        else:
            print("No contract address provided. Using USDT as example.")
            print("Usage: python examples/gulltoppr_example.py <contract_address> [rpc_url]")
            print()
            contract_address = examples["USDT"]
            rpc_url = None
        
        # Analyze contract
        client.analyze_contract(contract_address, rpc_url)
        
        print("\n" + "=" * 60)
        print("Integration test completed successfully!")
        print("=" * 60)
        
    except FileNotFoundError:
        print("Error: gulltoppr-config.json not found")
        print("Please ensure you're running from the project root directory")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
