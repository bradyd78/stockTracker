import os
import sys
import requests
import time
from datetime import datetime

WATCHLIST_FILE = "watchlist.txt"
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
API_URL = "https://www.alphavantage.co/query"

def load_watchlist():
    if not os.path.exists(WATCHLIST_FILE):
        return []
    with open(WATCHLIST_FILE, "r") as f:
        return [line.strip().upper() for line in f if line.strip()]

def save_watchlist(symbols):
    with open(WATCHLIST_FILE, "w") as f:
        for symbol in symbols:
            f.write(symbol + "\n")

def add_stock(symbol):
    symbols = load_watchlist()
    symbol = symbol.upper()
    if symbol not in symbols:
        symbols.append(symbol)
        save_watchlist(symbols)
        print(f"Added {symbol} to your watchlist.")
    else:
        print(f"{symbol} is already in your watchlist.")

def remove_stock(symbol):
    symbols = load_watchlist()
    symbol = symbol.upper()
    if symbol in symbols:
        symbols.remove(symbol)
        save_watchlist(symbols)
        print(f"Removed {symbol} from your watchlist.")
    else:
        print(f"{symbol} is not in your watchlist.")

def list_stocks():
    symbols = load_watchlist()
    if not symbols:
        print("Your watchlist is empty.")
        return
    print("Your watchlist:")
    for symbol in symbols:
        print(f"- {symbol}")

def fetch_stock_quote(symbol):
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": API_KEY
    }
    r = requests.get(API_URL, params=params)
    if r.status_code != 200:
        raise Exception("API request failed")
    data = r.json()
    if "Global Quote" not in data or not data["Global Quote"]:
        return None
    gq = data["Global Quote"]
    return {
        "symbol": gq["01. symbol"],
        "price": float(gq["05. price"]),
        "change": float(gq["09. change"]),
        "change_perc": gq["10. change percent"],
        "time": datetime.now().strftime("%H:%M")
    }

def show_stocks():
    symbols = load_watchlist()
    if not symbols:
        print("Your watchlist is empty.")
        return
    print("+-------+---------+---------+----------+--------+")
    print("| TICK  |  PRICE  |  CHANGE | % CHANGE |  TIME  |")
    print("+-------+---------+---------+----------+--------+")
    for symbol in symbols:
        try:
            quote = fetch_stock_quote(symbol)
            if not quote:
                print(f"| {symbol:5} | {'N/A':7} | {'N/A':7} | {'N/A':8} | {'--:--':6} |")
                continue
            print(f"| {quote['symbol']:<5} | {quote['price']:>7.2f} | {quote['change']:>7.2f} | {quote['change_perc']:>8} | {quote['time']:>6} |")
            # Alpha Vantage free tier has a 5 requests/min limit.
            time.sleep(12)
        except Exception as e:
            print(f"| {symbol:5} | {'ERROR':7} | {'ERROR':7} | {'ERROR':8} | {'--:--':6} |")
    print("+-------+---------+---------+----------+--------+")

def export_csv():
    try:
        import csv
    except ImportError:
        print("csv module required for export.")
        return
    symbols = load_watchlist()
    if not symbols:
        print("Your watchlist is empty.")
        return
    rows = []
    for symbol in symbols:
        try:
            quote = fetch_stock_quote(symbol)
            if not quote:
                continue
            rows.append(quote)
            time.sleep(12)
        except Exception:
            continue
    if not rows:
        print("No data to export.")
        return
    with open("stocks_export.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["symbol", "price", "change", "change_perc", "time"])
        writer.writeheader()
        writer.writerows(rows)
    print("Exported tracked data to stocks_export.csv.")

def usage():
    print("Usage:")
    print("  python stock_tracker.py add SYMBOL")
    print("  python stock_tracker.py remove SYMBOL")
    print("  python stock_tracker.py list")
    print("  python stock_tracker.py show")
    print("  python stock_tracker.py export")

if __name__ == "__main__":
    if not API_KEY:
        print("Please set the ALPHA_VANTAGE_API_KEY environment variable.")
        sys.exit(1)
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)
    cmd = sys.argv[1].lower()
    if cmd == "add" and len(sys.argv) == 3:
        add_stock(sys.argv[2])
    elif cmd == "remove" and len(sys.argv) == 3:
        remove_stock(sys.argv[2])
    elif cmd == "list":
        list_stocks()
    elif cmd == "show":
        show_stocks()
    elif cmd == "export":
        export_csv()
    else:
        usage()
