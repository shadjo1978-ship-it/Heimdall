/**
 * Example script demonstrating Gulltoppr integration with Heimdall.
 * 
 * This script shows how to:
 * 1. Connect to the Gulltoppr service
 * 2. Analyze smart contracts
 * 3. Generate ABIs
 * 4. Handle responses
 * 
 * Usage:
 *   node examples/gulltoppr_example.js [contract_address] [rpc_url]
 */

const fs = require('fs');
const http = require('http');
const https = require('https');
const url = require('url');

class GulltopprClient {
  /**
   * Initialize the Gulltoppr client with configuration.
   * @param {string} configPath - Path to configuration file
   */
  constructor(configPath = 'gulltoppr-config.json') {
    const configData = fs.readFileSync(configPath, 'utf8');
    const config = JSON.parse(configData);
    
    this.config = config.gulltoppr;
    this.serviceUrl = this.config.service_url;
    this.defaultRpcUrl = this.config.default_rpc_url;
    this.timeout = this.config.timeout;
    
    if (!this.config.enabled) {
      throw new Error('Gulltoppr integration is disabled in configuration');
    }
  }

  /**
   * Check if Gulltoppr service is running.
   * @returns {Promise<boolean>}
   */
  async healthCheck() {
    return new Promise((resolve) => {
      const protocol = this.serviceUrl.startsWith('https') ? https : http;
      
      const req = protocol.get(this.serviceUrl, { timeout: this.timeout }, (res) => {
        resolve(res.statusCode === 200);
      });
      
      req.on('error', (err) => {
        console.error(`Health check failed: ${err.message}`);
        resolve(false);
      });
      
      req.on('timeout', () => {
        req.destroy();
        console.error('Health check timed out');
        resolve(false);
      });
    });
  }

  /**
   * Generate ABI for a smart contract.
   * @param {string} contractAddress - Ethereum contract address (0x...)
   * @param {string|null} rpcUrl - RPC endpoint URL (optional)
   * @returns {Promise<Object>}
   */
  async generateAbi(contractAddress, rpcUrl = null) {
    if (!contractAddress.startsWith('0x')) {
      throw new Error('Contract address must start with 0x');
    }

    const rpc = rpcUrl || this.defaultRpcUrl;
    const requestUrl = `${this.serviceUrl}/${contractAddress}?rpc_url=${encodeURIComponent(rpc)}`;
    
    return new Promise((resolve, reject) => {
      const protocol = requestUrl.startsWith('https') ? https : http;
      
      const req = protocol.get(requestUrl, { timeout: this.timeout }, (res) => {
        let data = '';
        
        res.on('data', (chunk) => {
          data += chunk;
        });
        
        res.on('end', () => {
          if (res.statusCode === 200) {
            try {
              resolve(JSON.parse(data));
            } catch (err) {
              reject(new Error(`Failed to parse response: ${err.message}`));
            }
          } else {
            reject(new Error(`HTTP ${res.statusCode}: ${data}`));
          }
        });
      });
      
      req.on('error', (err) => {
        reject(new Error(`Request failed: ${err.message}`));
      });
      
      req.on('timeout', () => {
        req.destroy();
        reject(new Error('Request timed out'));
      });
    });
  }

  /**
   * Analyze a smart contract and print results.
   * @param {string} contractAddress - Ethereum contract address
   * @param {string|null} rpcUrl - RPC endpoint URL (optional)
   */
  async analyzeContract(contractAddress, rpcUrl = null) {
    console.log(`Analyzing contract: ${contractAddress}`);
    console.log('-'.repeat(60));
    
    try {
      const result = await this.generateAbi(contractAddress, rpcUrl);
      
      console.log('✓ Analysis complete!');
      console.log(`Contract: ${contractAddress}`);
      
      if (result.abi) {
        console.log(`ABI generated with ${result.abi.length} functions`);
        console.log('\nABI Preview:');
        console.log(JSON.stringify(result.abi.slice(0, 3), null, 2));
        if (result.abi.length > 3) {
          console.log(`... and ${result.abi.length - 3} more functions`);
        }
      }
      
      console.log('\nFull result saved to: contract_analysis.json');
      fs.writeFileSync('contract_analysis.json', JSON.stringify(result, null, 2));
      
    } catch (err) {
      console.error(`✗ Analysis failed: ${err.message}`);
      throw err;
    }
  }
}

/**
 * Main function demonstrating Gulltoppr usage.
 */
async function main() {
  // Example contract addresses (well-known contracts)
  const examples = {
    USDT: '0xdac17f958d2ee523a2206206994597c13d831ec7',
    USDC: '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48',
    DAI: '0x6b175474e89094c44da98b954eedeac495271d0f'
  };
  
  console.log('='.repeat(60));
  console.log('Gulltoppr Integration Example');
  console.log('='.repeat(60));
  console.log();
  
  try {
    // Initialize client
    const client = new GulltopprClient();
    
    // Health check
    console.log('Checking Gulltoppr service...');
    const isHealthy = await client.healthCheck();
    
    if (isHealthy) {
      console.log('✓ Gulltoppr service is running\n');
    } else {
      console.log('✗ Gulltoppr service is not available');
      console.log('Please ensure Gulltoppr is running:');
      console.log('  docker-compose up -d');
      process.exit(1);
    }
    
    // Get contract address from command line or use example
    const args = process.argv.slice(2);
    let contractAddress, rpcUrl;
    
    if (args.length > 0) {
      contractAddress = args[0];
      rpcUrl = args.length > 1 ? args[1] : null;
    } else {
      console.log('No contract address provided. Using USDT as example.');
      console.log('Usage: node examples/gulltoppr_example.js <contract_address> [rpc_url]');
      console.log();
      contractAddress = examples.USDT;
      rpcUrl = null;
    }
    
    // Analyze contract
    await client.analyzeContract(contractAddress, rpcUrl);
    
    console.log('\n' + '='.repeat(60));
    console.log('Integration test completed successfully!');
    console.log('='.repeat(60));
    
  } catch (err) {
    if (err.code === 'ENOENT') {
      console.error('Error: gulltoppr-config.json not found');
      console.error('Please ensure you\'re running from the project root directory');
    } else {
      console.error(`Error: ${err.message}`);
    }
    process.exit(1);
  }
}

// Run main function
if (require.main === module) {
  main();
}

module.exports = { GulltopprClient };
