# stockTracker

stockTracker is a Python-based application that allows users to track the prices and performance of stocks in real-time or over time. The tool is designed for individual investors, traders, or anyone interested in monitoring the stock market, managing watchlists, and analyzing basic metrics. It fetches data from public APIs and provides a simple command-line interface for adding, removing, and viewing tracked stocks.

## Features

- Track real-time stock prices and historical performance
- Simple watchlist management (add/remove/list stocks)
- Fetches data from free, public stock APIs (e.g., Alpha Vantage, Yahoo Finance)
- Basic analytics (price change, percentage change, high/low over period)
- Export tracked data to CSV
- Command-line interface for ease of use

## Requirements

- Python 3.8+
- `requests` library
- (Optional) `pandas` for CSV export
- Free API key from a supported stock data provider (e.g., Alpha Vantage)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/bradyd78/stockTracker.git
   cd stockTracker
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Obtain a free API key from [Alpha Vantage](https://www.alphavantage.co/support/#api-key) or another supported provider.

4. Set your API key as an environment variable:
   ```bash
   export ALPHA_VANTAGE_API_KEY=your_api_key_here
   ```

## Usage

- Add a stock to your watchlist:
  ```bash
  python stock_tracker.py add AAPL
  ```

- Remove a stock from your watchlist:
  ```bash
  python stock_tracker.py remove TSLA
  ```

- List all tracked stocks:
  ```bash
  python stock_tracker.py list
  ```

- Show the latest price and metrics for your watchlist:
  ```bash
  python stock_tracker.py show
  ```

- Export tracked data to CSV:
  ```bash
  python stock_tracker.py export
  ```

## Example

```
$ python stock_tracker.py add MSFT
Added MSFT to your watchlist.

$ python stock_tracker.py show
+-------+---------+---------+----------+--------+
| TICK  |  PRICE  |  CHANGE | % CHANGE |  TIME  |
+-------+---------+---------+----------+--------+
| MSFT  |  400.25 |   +2.15 |   +0.54% | 16:35  |
+-------+---------+---------+----------+--------+
```

## Configuration

- All tracked symbols are stored in a local file (`watchlist.txt`) by default.
- API key is read from the environment variable `ALPHA_VANTAGE_API_KEY`.

## License

MIT License

## Disclaimer

This tool is for educational and informational purposes only. Stock data is provided by third-party APIs and may be delayed or inaccurate. Do not use this tool for trading or investment decisions.
