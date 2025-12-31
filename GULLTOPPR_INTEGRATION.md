# Gulltoppr Integration Guide

## Overview

Gulltoppr is a Rust-based backend service that provides fast and efficient EVM (Ethereum Virtual Machine) smart contract bytecode analysis. It's built using the Actix web framework and leverages the heimdall-rs toolkit for advanced contract analysis capabilities.

## What is Gulltoppr?

Gulltoppr powers services like [abi.ninja](https://abi.ninja) and provides:

- **ABI Generation**: Automatically generate Application Binary Interfaces (ABIs) from contract addresses
- **Bytecode Decompilation**: Analyze and understand smart contract bytecode
- **Fast Performance**: Written in Rust for optimal speed and memory safety
- **Simple API**: Easy-to-use REST endpoints for contract analysis

## Architecture

```
┌─────────────┐         ┌─────────────┐         ┌──────────────┐
│  Heimdall   │ ◄─────► │  Gulltoppr  │ ◄─────► │ Ethereum RPC │
│     AI      │         │   Service   │         │   Provider   │
└─────────────┘         └─────────────┘         └──────────────┘
```

Heimdall can leverage Gulltoppr to analyze smart contracts, providing enhanced capabilities for blockchain security analysis and smart contract interaction.

## Installation

### Option 1: Docker Compose (Recommended)

The simplest way to get started:

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f gulltoppr

# Stop services
docker-compose down
```

### Option 2: Build from Source

For development or customization:

```bash
# Install Rust (if not already installed)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Clone and build Gulltoppr
git clone https://github.com/portdeveloper/gulltoppr.git
cd gulltoppr
cargo build --release

# Run the service
cargo run --release
```

### Option 3: Docker Only

```bash
docker pull portdeveloper/gulltoppr:latest
docker run -d -p 8080:8080 --name gulltoppr portdeveloper/gulltoppr:latest
```

## API Endpoints

### Health Check

**Endpoint:** `GET /`

**Description:** Returns a greeting to verify the service is running.

**Example:**
```bash
curl http://localhost:8080/
```

**Response:**
```
Hello from Gulltoppr!
```

### Generate ABI

**Endpoint:** `GET /{contract_address}?rpc_url={rpc_url}`

**Description:** Generates an ABI for the specified smart contract address.

**Parameters:**
- `contract_address`: Ethereum contract address (0x...)
- `rpc_url`: Ethereum RPC endpoint URL (query parameter)

**Example:**
```bash
# Analyze a contract on Ethereum mainnet
curl "http://localhost:8080/0x1234567890123456789012345678901234567890?rpc_url=https://eth.llamarpc.com"
```

**Response:**
```json
{
  "abi": [...],
  "contract_address": "0x1234567890123456789012345678901234567890",
  "analysis": {...}
}
```

## Configuration

The `gulltoppr-config.json` file contains integration settings:

```json
{
  "gulltoppr": {
    "enabled": true,
    "service_url": "http://localhost:8080",
    "default_rpc_url": "eth.llamarpc.com",
    "timeout": 30000
  }
}
```

### Configuration Options

- **enabled**: Enable/disable Gulltoppr integration (boolean)
- **service_url**: URL where Gulltoppr is running (string)
- **default_rpc_url**: Default Ethereum RPC provider with protocol (string, e.g., `https://eth.llamarpc.com`)
- **timeout**: Request timeout in milliseconds (number)

### Popular RPC Providers

- `https://eth.llamarpc.com` - LlamaNodes (free)
- `https://rpc.ankr.com/eth` - Ankr
- `https://cloudflare-eth.com` - Cloudflare
- Your own Infura/Alchemy endpoint

## Use Cases

### 1. Smart Contract Security Analysis

Analyze contracts for security vulnerabilities before interaction:

```bash
curl "http://localhost:8080/0xContractAddress?rpc_url=https://eth.llamarpc.com"
```

### 2. ABI Discovery

Automatically generate ABIs for contracts without verified source code:

```bash
curl "http://localhost:8080/0xUnverifiedContract?rpc_url=https://eth.llamarpc.com"
```

### 3. Contract Function Discovery

Discover available functions and their signatures in any deployed contract.

## Troubleshooting

### Service not responding

```bash
# Check if service is running
docker ps | grep gulltoppr

# Or check the process
ps aux | grep gulltoppr

# Restart the service
docker-compose restart gulltoppr
```

### Connection refused

Ensure Gulltoppr is running on the correct port:

```bash
# Check port 8080
netstat -tuln | grep 8080

# Or with lsof
lsof -i :8080
```

### RPC errors

If you get RPC-related errors:
- Verify your RPC URL is accessible
- Check rate limits on your RPC provider
- Try an alternative RPC endpoint

## Performance Considerations

- **Caching**: Consider implementing caching for frequently analyzed contracts
- **Rate Limiting**: Some RPC providers have rate limits; monitor usage
- **Resource Usage**: Gulltoppr is lightweight but bytecode analysis can be CPU-intensive for large contracts

## Security Notes

- Run Gulltoppr in an isolated network environment
- Use trusted RPC providers only
- Validate contract addresses before analysis
- Keep Gulltoppr updated for latest security patches

## Additional Resources

- [Gulltoppr GitHub Repository](https://github.com/portdeveloper/gulltoppr)
- [heimdall-rs Toolkit](https://github.com/Jon-Becker/heimdall-rs)
- [abi.ninja](https://abi.ninja) - Production example using Gulltoppr

## Support

For issues specific to:
- **Gulltoppr**: Open an issue at [portdeveloper/gulltoppr](https://github.com/portdeveloper/gulltoppr/issues)
- **Heimdall Integration**: Open an issue in this repository

## License

Gulltoppr is licensed under the MIT License. See the [Gulltoppr repository](https://github.com/portdeveloper/gulltoppr) for details.
