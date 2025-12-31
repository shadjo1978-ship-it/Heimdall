#!/bin/bash
# Quick test script for Gulltoppr integration

set -e

echo "========================================"
echo "Gulltoppr Integration Test"
echo "========================================"
echo

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
GULLTOPPR_URL="${GULLTOPPR_URL:-http://localhost:8080}"
TEST_CONTRACT="${1:-0xdac17f958d2ee523a2206206994597c13d831ec7}" # USDT by default
RPC_URL="${2:-https://eth.llamarpc.com}"

# Function to check if Gulltoppr is running
check_service() {
    echo "Checking Gulltoppr service at ${GULLTOPPR_URL}..."
    if curl -f -s "${GULLTOPPR_URL}/" > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} Gulltoppr service is running"
        return 0
    else
        echo -e "${RED}✗${NC} Gulltoppr service is not available"
        return 1
    fi
}

# Function to analyze a contract
analyze_contract() {
    local contract=$1
    local rpc=$2
    
    echo
    echo "Analyzing contract: ${contract}"
    echo "Using RPC: ${rpc}"
    echo "----------------------------------------"
    
    local url="${GULLTOPPR_URL}/${contract}?rpc_url=${rpc}"
    
    if response=$(curl -f -s "${url}" 2>&1); then
        echo -e "${GREEN}✓${NC} Analysis complete!"
        echo
        echo "Response preview:"
        echo "${response}" | head -c 500
        echo
        echo "..."
        echo
        echo "Full response saved to: gulltoppr_response.json"
        echo "${response}" | jq '.' > gulltoppr_response.json 2>/dev/null || echo "${response}" > gulltoppr_response.json
        return 0
    else
        echo -e "${RED}✗${NC} Analysis failed"
        echo "Error: ${response}"
        return 1
    fi
}

# Main execution
main() {
    # Check if service is running
    if ! check_service; then
        echo
        echo -e "${YELLOW}Note:${NC} To start Gulltoppr, run:"
        echo "  docker-compose up -d"
        echo
        echo "Or build from source:"
        echo "  git clone https://github.com/portdeveloper/gulltoppr.git"
        echo "  cd gulltoppr"
        echo "  cargo run"
        exit 1
    fi
    
    # Analyze the contract
    if analyze_contract "${TEST_CONTRACT}" "${RPC_URL}"; then
        echo
        echo "========================================"
        echo -e "${GREEN}Integration test passed!${NC}"
        echo "========================================"
        exit 0
    else
        echo
        echo "========================================"
        echo -e "${RED}Integration test failed!${NC}"
        echo "========================================"
        exit 1
    fi
}

# Show usage if help is requested
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    echo "Usage: $0 [contract_address] [rpc_url]"
    echo
    echo "Arguments:"
    echo "  contract_address  Ethereum contract address (default: USDT)"
    echo "  rpc_url          RPC endpoint URL (default: https://eth.llamarpc.com)"
    echo
    echo "Environment variables:"
    echo "  GULLTOPPR_URL    Gulltoppr service URL (default: http://localhost:8080)"
    echo
    echo "Examples:"
    echo "  $0"
    echo "  $0 0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
    echo "  $0 0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48 https://eth.llamarpc.com"
    echo "  GULLTOPPR_URL=http://gulltoppr:8080 $0"
    exit 0
fi

# Run main function
main
