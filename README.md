# Blockchain Transaction Tracing Tool

## Overview

This Python script is designed to trace the movement of funds on the Ethereum blockchain. It monitors transactions in real-time by scanning newly mined blocks, as well as querying specific blocks for transactions involving an address provided by the user. The script retrieves both direct and internal transactions and provides detailed information about the transactions.  It is an introductory tool with principles that can be expanded upon to build more advanced blockchain forensics and monitoring solutions. 

## Features

* Monitor new blocks in real-time for transactions involving a specific Ethereum address.
* Query a block for direct and internal transactions involving a target address.
* Display transaction details such as sender, receiver, value, and transaction type.
* Handles internal transactions, including smart contract calls and contract interactions.
* Provides clear error handling and output formatting.

## Requirements

Before using the script, ensure you have the following installed:

* **Python 3.x**: The script is written in Python 3.7 and higher.
* **Web3.py**: Python library to interact with the blockchain.
* **Requests**: For making HTTP requests to interact with Ethereum nodes.

You can install the required dependencies by running the following commands:

```
pip install web3 requests
```
## Setup

### 1. Clone the repository

Clone this repository to your local machine or create a new Python script using the following template.

```
git clone <repository-url>
cd <repository-directory>
```
### 2. Set up an Ethereum Node Provider

The script uses an Ethereum node to interact with the blockchain. You can connect to either your local Ethereum node or a public node provider like Infura, Alchemy, or QuickNode.

Once you've signed up for a node provider, you'll receive an API endpoint (RPC URL). Add this URL to the script where RPC_URL is defined:

```
RPC_URL = "<Your-Ethereum-Node-URL>"
```
Optionally you can use the following endpoint: https://rpc.ankr.com/eth

### 3. Running the script

To run the script, simply execute the following command:

```
python detect.py
```
This will start the program and prompt you for input.

## How It Works

### 1. Input Ethereum Address
Upon execution, the script will first ask you for an address. If you provide an invalid address, it will keep prompting you for a valid address.

### 2. Choose an Option
Once a valid address is provided, you will be given three options:

* **Monitor new blocks in real-time**: Continuously monitors new blocks for transactions involving the specified address. The script fetches both direct and internal transactions for each new block mined.
* **Query a specific block**: You can query a specific block for transactions involving the provided address. You need to input a block number, and the script will return the relevant transactions.
* **Exit**: Exit the script.

### 3. Monitor Real-Time Transactions
If you select the option to monitor new blocks, the script will start an infinite loop, checking new blocks for transactions every 5 seconds. It will list all detected transactions involving the specified address, including direct transactions and internal transfers.

### 4. Query Specific Block
If you select to query a specific block, you will be prompted for the block number. The script will fetch that block and list the transactions that involve the given address.

## Example Output

### Real-time Monitoring

If the address has transactions in the newly mined blocks, you will see output like the following:

```
Monitoring block 1234567 for transactions...

Detected transactions in block 1234567:

Transaction Type: Direct
Transaction Hash: 0x123abc...
From Address: 0xabc123...
To Address: 0xdef456...
Value of sent ether: 5.0 ETH

---------------------------------------------------------
```

If no transactions are detected in a block:

```
No transactions detected in block 1234567.
```

### Querying Specific Block

If you query a specific block, the output will be similar to the following:

```
Querying block 1234567...

Detected transactions in block 1234567:
Transaction Type: Direct
Transaction Hash: 0x123abc...
From Address: 0xabc123...
To Address: 0xdef456...
Value of sent ether: 3.2 ETH

---------------------------------------------------------
```

## Troubleshooting

* **Error retrieving block dat**a: If you encounter errors when fetching block data, ensure that your Ethereum node or RPC endpoint is working correctly and your network connection is stable.

* **Internal Transaction Tracing Issues**: If the script does not detect internal transactions, ensure that the Ethereum node you are using supports the **debug_traceBlockByNumber** method, as some public nodes may restrict access to advanced RPC methods.

## Contributions

Feel free to contribute to the development of this script by creating issues or pull requests. Contributions can include:

* Improving the error handling and edge cases.
* Adding support for other blockchains.
* Adding support for token transfers.

## License

This project is open-source and available under the [MIT License](https://en.wikipedia.org/wiki/MIT_License)





