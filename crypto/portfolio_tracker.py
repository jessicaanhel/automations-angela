import requests
import os
from dotenv import load_dotenv
import schedule
import time
from telegram import Bot
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from datetime import datetime

load_dotenv()

COVALENT_API_KEY = os.getenv("COVALENT_API_KEY")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
GOOGLE_CREDENTIALS_FILE = os.getenv("GOOGLE_SHEET_CREDENTIALS_FILE")
BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
METAMASK_ADDRESS = os.getenv("METAMASK_ADDRESS")
TRUSTWALLET_ADDRESS = os.getenv("TRUSTWALLET_ADDRESS")

COIN = 'PEPE'

bot = Bot(token=TELEGRAM_BOT_TOKEN)

def get_bybit_balance():
    url = f"https://api.bybit.com/v2/private/wallet/balance"
    params = {
        "api_key": BYBIT_API_KEY,
        "coin": COIN,
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data["ret_code"] == 0:
        return f"Bybit COIN Balance: {data['result'][COIN]['available_balance']} COIN"
    return "Error fetching Bybit balance."


def get_binance_balance():
    url = "https://api.binance.com/api/v3/account"
    headers = {"X-MBX-APIKEY": BINANCE_API_KEY}
    response = requests.get(url, headers=headers)
    data = response.json()
    if 'balances' in data:
        coin_balance = next((item for item in data['balances'] if item['asset'] == COIN), None)
        return f"Binance COIN Balance: {coin_balance['free']} COIN" if coin_balance else "No COIN balance found."
    return "Error fetching Binance balance."


def get_ethereum_balance(address, covalent_api_key):
    url = f"https://api.covalenthq.com/v1/1/address/{address}/balances_v2/"
    params = {
        "key": covalent_api_key,
    }
    response = requests.get(url, params=params)
    data = response.json()

    if "data" in data and "items" in data["data"]:
        eth_balance = next(
            (item for item in data["data"]["items"] if item["contract_ticker_symbol"] == "ETH"), None
        )
        if eth_balance:
            return f"Ethereum Wallet Balance: {float(eth_balance['balance']) / 10**18:.4f} ETH"

    return "Error fetching Ethereum balance."



def get_wallet_data():
    bybit_balance = get_bybit_balance()
    binance_balance = get_binance_balance()
    metamask_balance = get_ethereum_balance(METAMASK_ADDRESS, COVALENT_API_KEY)
    trustwallet_balance = get_ethereum_balance(TRUSTWALLET_ADDRESS, COVALENT_API_KEY)

    return f"{bybit_balance}\n{binance_balance}\n{metamask_balance}\n{trustwallet_balance}"

def fetch_portfolio_data():
    bybit_balance = get_bybit_balance()
    binance_balance = get_binance_balance()
    metamask_balance = get_ethereum_balance(METAMASK_ADDRESS, ETHERSCAN_API_KEY)
    trustwallet_balance = get_ethereum_balance(TRUSTWALLET_ADDRESS, ETHERSCAN_API_KEY)

    return {
        "Bybit Balance": bybit_balance,
        "Binance Balance": binance_balance,
        "MetaMask Balance": metamask_balance,
        "Trust Wallet Balance": trustwallet_balance
    }

def send_telegram_report(portfolio_data):
    report_message = "📊 *Portfolio Tracker Summary*:\n"
    for wallet, balance in portfolio_data.items():
        report_message += f"{wallet}: {balance}\n"
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=report_message)


def update_google_sheet(portfolio_data):
    creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=["https://www.googleapis.com/auth/spreadsheets"])
    service = build('sheets', 'v4', credentials=creds)

    sheet = service.spreadsheets()

    values = [["Date", "Wallet", "Balance"]]
    for wallet, balance in portfolio_data.items():
        values.append([datetime.today().strftime('%Y-%m-%d'), wallet, balance])

    body = {"values": values}

    result = sheet.values().append(
        spreadsheetId=GOOGLE_SHEET_ID,
        range="A1:C1",
        valueInputOption="RAW",
        body=body
    ).execute()


def track_portfolio():
    portfolio_data = fetch_portfolio_data()
    send_telegram_report(portfolio_data)
    update_google_sheet(portfolio_data)


# Schedule the tracking: Run daily at 9 AM
schedule.every().day.at("09:00").do(track_portfolio)


if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(60)