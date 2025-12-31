# Heimdall
A.I personal assistant with real time thinking and voice also serves as a firewall

## Features

- Real-time AI processing and thinking
- Voice interaction capabilities
- Firewall functionality
- **Gulltoppr Integration**: EVM smart contract bytecode analysis and ABI generation

## Gulltoppr Integration

Heimdall integrates with [Gulltoppr](https://github.com/portdeveloper/gulltoppr), a high-performance Rust backend for EVM smart contract analysis. This integration provides:

- **Smart Contract ABI Generation**: Automatically generate ABIs from contract addresses
- **Bytecode Analysis**: Analyze EVM bytecode for security and functionality insights
- **Fast Processing**: Leverages Rust and Actix framework for optimal performance

### Quick Start with Gulltoppr

#### Using Docker Compose

The easiest way to run Heimdall with Gulltoppr is using Docker Compose:

```bash
docker-compose up -d
```

This will start the Gulltoppr service on `http://localhost:8080`.

#### Manual Setup

If you prefer to run Gulltoppr separately:

1. Clone the Gulltoppr repository:
```bash
git clone https://github.com/portdeveloper/gulltoppr.git
cd gulltoppr
```

2. Build and run with Cargo:
```bash
cargo build
cargo run
```

Or use Docker:
```bash
docker build -t gulltoppr .
docker run -p 8080:8080 gulltoppr
```

### Using Gulltoppr

Once running, you can use Gulltoppr to analyze smart contracts:

**Health Check:**
```bash
curl http://localhost:8080/
```

**Generate ABI for a contract:**
```bash
curl http://localhost:8080/0xYourContractAddress?rpc_url=https://eth.llamarpc.com
```

### Configuration

Gulltoppr settings can be customized in `gulltoppr-config.json`:

- `service_url`: URL where Gulltoppr service is running (default: `http://localhost:8080`)
- `default_rpc_url`: Default Ethereum RPC URL for contract queries (default: `https://eth.llamarpc.com`)
- `timeout`: Request timeout in milliseconds (default: `30000`)

## License

See individual component licenses for details.
