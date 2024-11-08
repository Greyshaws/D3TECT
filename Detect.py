from web3 import Web3
import requests
from colorama import Fore, Style
import time

RPC_URL = "https://rpc.ankr.com/eth"

# Initialize a connection
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Check connection status
print(f'{Fore.WHITE}---------------------------------------------------------\n')

if w3.is_connected():
    print(f'{Fore.GREEN}Connected to the blockchain{Style.RESET_ALL}')
else:
    print(f'{Fore.RED}Failed to connect{Style.RESET_ALL}')
    exit()

print()
print(f'{Fore.WHITE}---------------------------------------------------------\n')
print()

# Retrieve all transactions in the block and filter for direct transfers
def get_direct_transfers(block_number, target_address):
    try:
        block = w3.eth.get_block(block_number, full_transactions=True)
        transfers = []

        for tx in block.transactions:
            from_address = tx["from"].lower()
            to_address = (tx["to"] or "").lower()  # 'to' can be None if it's a contract creation
            value = tx["value"] / 10**18  # Convert from wei to ether

            if from_address == target_address or to_address == target_address:
                transfers.append({
                    "transaction_hash": "0x" + tx["hash"].hex(),
                    "from_address": from_address,
                    "to_address": to_address,
                    "value": value,
                    "type": "Direct"
                })

        return transfers
    except Exception as e:
        print(f"{Fore.RED}Error retrieving block data: {e}{Style.RESET_ALL}")
        return []

# Trace transactions using debug_traceBlockByNumber
def trace_block_by_number(block_number):
    method = "debug_traceBlockByNumber"
    params = [hex(block_number), {"tracer": "callTracer", "timeout": "10s"}]
    
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1
    }
    
    try:
        response = requests.post(RPC_URL, headers={'Content-Type': 'application/json'}, json=payload)
        if response.status_code == 200:
            return response.json().get("result", [])
        else:
            print(f"{Fore.RED}Error retrieving traces: {response.status_code}, {response.text}{Style.RESET_ALL}")
            return None
    except requests.RequestException as e:
        print(f"{Fore.RED}Error connecting to Ethereum node: {e}{Style.RESET_ALL}")
        return None

# Recursively trace calls to detect transfers involving the specified address
def trace_calls_for_address(trace, tx_hash, target_address):
    result = trace.get("result", {})
    
    from_address = result.get("from", "Unknown").lower()
    to_address = result.get("to", "Unknown").lower()
    value_hex = result.get("value", "0x0")
    value = int(value_hex, 16) / 10**18  # Convert from wei to ether

    transfers = []
    if from_address == target_address or to_address == target_address:
        transfers.append({
            "transaction_hash": tx_hash,
            "from_address": from_address,
            "to_address": to_address,
            "value": value,
            "type": "Internal"
        })

    if "calls" in result:
        for call in result["calls"]:
            transfers.extend(trace_calls_for_address({"result": call}, tx_hash, target_address))

    return transfers

# Detect transfers involving the specified address in trace results
def detect_transfers_for_address(trace_result, target_address):
    detected_transfers = []

    for trace in trace_result:
        try:
            tx_hash = trace.get("txHash")
            transfers = trace_calls_for_address(trace, tx_hash, target_address)
            detected_transfers.extend(transfers)
        except Exception as e:
            print(f"{Fore.RED}Error processing trace: {e}{Style.RESET_ALL}")
            print("Trace data causing the error:", trace)

    return detected_transfers

# Real-time monitoring loop
def monitor_real_time(target_address):
    latest_block = w3.eth.block_number

    while True:
        block_number = latest_block
        print()
        print(f"{Fore.YELLOW}Monitoring block {block_number} for transactions...{Style.RESET_ALL}")
        
        # Get direct transfers in the latest block
        direct_transfers = get_direct_transfers(block_number, target_address)

        # Trace the block for internal transactions
        trace_result = trace_block_by_number(block_number)
        internal_transfers = []

        if trace_result:
            internal_transfers = detect_transfers_for_address(trace_result, target_address)

        all_transfers = direct_transfers + internal_transfers

        if all_transfers:
            print(f"\n{Fore.GREEN}Detected transactions in block {block_number}:{Style.RESET_ALL}")
            for transfer in all_transfers:
                print()
                print(f"{Fore.BLUE}Transaction Type:{Style.RESET_ALL} {transfer['type']}")
                print(f"{Fore.BLUE}Transaction Hash:{Style.RESET_ALL} {transfer['transaction_hash']}")
                print(f"{Fore.BLUE}From Address:{Style.RESET_ALL} {transfer['from_address']}")
                print(f"{Fore.BLUE}To Address:{Style.RESET_ALL} {transfer['to_address']}")
                print(f"{Fore.BLUE}Value of sent ether:{Style.RESET_ALL} {transfer['value']} ETH")
                print()
                print(f'{Fore.WHITE}---------------------------------------------------------')
        else:
            print(f"\n{Fore.RED}No transactions detected in block {block_number}.{Style.RESET_ALL}")

        latest_block += 1
        time.sleep(5)  # Delay before checking the next block

# Query a specific block
def query_specific_block(target_address):
    while True:
        block_number = input(f"{Fore.YELLOW}Enter block number: {Style.RESET_ALL}")
        try:
            block_number = int(block_number)
            break
        except ValueError:
            print(f"{Fore.RED}Invalid block number. Please try again.{Style.RESET_ALL}")
    
    print()
    print(f"{Fore.YELLOW}Querying block {block_number} for transactions...{Style.RESET_ALL}")

    # Get direct transfers in the specified block
    direct_transfers = get_direct_transfers(block_number, target_address)

    # Trace the block for internal transactions
    trace_result = trace_block_by_number(block_number)
    internal_transfers = []

    if trace_result:
        internal_transfers = detect_transfers_for_address(trace_result, target_address)

    all_transfers = direct_transfers + internal_transfers

    if all_transfers:
        print(f"\n{Fore.GREEN}Detected transactions in block {block_number}:{Style.RESET_ALL}")
        for transfer in all_transfers:
            print()
            print(f"{Fore.BLUE}Transaction Type:{Style.RESET_ALL} {transfer['type']}")
            print(f"{Fore.BLUE}Transaction Hash:{Style.RESET_ALL} {transfer['transaction_hash']}")
            print(f"{Fore.BLUE}From Address:{Style.RESET_ALL} {transfer['from_address']}")
            print(f"{Fore.BLUE}To Address:{Style.RESET_ALL} {transfer['to_address']}")
            print(f"{Fore.BLUE}Value of sent ether:{Style.RESET_ALL} {transfer['value']} ETH")
            print()
            print(f'{Fore.WHITE}---------------------------------------------------------')
    else:
        print(f"\n{Fore.RED}No transactions detected in block {block_number}.{Style.RESET_ALL}")

def main():
    while True:
        address = input(f"{Fore.YELLOW}Enter the address: {Style.RESET_ALL}").strip().lower()
        if not w3.is_address(address):
            print(f"{Fore.RED}Invalid address. Please try again.{Style.RESET_ALL}")
            continue
        else:
            break
    
    while True:
        print(f"\n{Fore.YELLOW}Choose an option:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}1. Monitor new blocks in real-time")
        print(f"{Fore.CYAN}2. Query a specific block")
        print(f"{Fore.RED}3. Exit{Style.RESET_ALL}")
        print()
        
        choice = input(f"{Fore.YELLOW}Enter your choice (1/2/3): {Style.RESET_ALL}")
        print()

        if choice == "1":
            print(f"{Fore.YELLOW}Fetching transactions for address {address}...{Style.RESET_ALL}")
            monitor_real_time(address)
        elif choice == "2":
            query_specific_block(address)
        elif choice == "3":
            print(f"{Fore.RED}Exiting...{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
