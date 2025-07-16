from flask import Flask, request, jsonify
from stock_tracker import load_watchlist, add_stock, remove_stock, fetch_stock_quote

app = Flask(__name__)

@app.route("/api/watchlist", methods=["GET"])
def get_watchlist():
    return jsonify(load_watchlist())

@app.route("/api/watchlist", methods=["POST"])
def post_watchlist():
    data = request.get_json()
    symbol = data.get("symbol", "").upper()
    add_stock(symbol)
    return jsonify({"message": f"{symbol} added."})

@app.route("/api/watchlist/<symbol>", methods=["DELETE"])
def delete_watchlist(symbol):
    remove_stock(symbol)
    return jsonify({"message": f"{symbol} removed."})

@app.route("/api/quote/<symbol>", methods=["GET"])
def get_quote(symbol):
    quote = fetch_stock_quote(symbol.upper())
    return jsonify(quote if quote else {})
