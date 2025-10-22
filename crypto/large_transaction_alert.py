import os
import requests
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()

RPC_URL = os.getenv("RPC_URL")
ALERT_THRESHOLD = float(os.getenv("ALERT_THRESHOLD", 100))
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

web3 = Web3(Web3.HTTPProvider(RPC_URL))

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, data=payload)

def handle_block(block_number):
    block = web3.eth.get_block(block_number, full_transactions=True)
    print(f"\n⛏️ New block: {block_number} ({len(block.transactions)} txs)")

    for tx in block.transactions:
        eth_value = web3.from_wei(tx.value, 'ether')
        if eth_value >= ALERT_THRESHOLD:
            msg = (
                f"<b>Large Transaction Detected</b>\n\n"
                f"<b>Tx Hash:</b> <a href='https://etherscan.io/tx/{tx.hash.hex()}'>{tx.hash.hex()}</a>\n"
                f"<b>From:</b> {tx['from']}\n"
                f"<b>To:</b> {tx['to']}\n"
                f"<b>Value:</b> {eth_value:.2f} ETH"
            )
            print(msg)
            send_telegram_alert(msg)

if not web3.is_connected():
    raise Exception("Web3 not connected")

print(f"Monitoring for ETH transactions over {ALERT_THRESHOLD} ETH...")

if __name__ == "__main__":
    last_block = web3.eth.block_number
    while True:
        current_block = web3.eth.block_number
        if current_block > last_block:
            for b in range(last_block + 1, current_block + 1):
                handle_block(b)
            last_block = current_block
