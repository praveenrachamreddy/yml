from upstox_api.api import *
from datetime import datetime
from pprint import pprint
import os, sys
from tempfile import gettempdir
from flask import Flask, request

app = Flask(__name__)

# Set up your Upstox API credentials

api_key = "e3fe3477-efac-4ff7-a0b9-3310a75d8fc8"
api_secret = "wvzzsquu14"
redirect_uri = "https://upstoxapi.awsdinesh.xyz/callback"
s = Session(api_key)
s.set_redirect_uri(redirect_uri)
s.set_api_secret(api_secret)
print(s.get_login_url())


@app.route('/callback')
def handle_callback():
    global access_token
    code = request.args.get('code')
    s.set_code(code)
    access_token = s.retrieve_access_token()
    # Now you have the access token, and you can proceed with using the Upstox API
    u = Upstox(api_key, access_token)

    return "Access token retrieved successfully!"






# Set the quantity for trading
quantity = 1
script = "NIFTY 18MAY23 18200 CE"

# Open log files
log = open("log.txt", "a")  # Open the file in append mode
execution = open("execution.txt", "a")  # Open the file in append mode
# Get the current timestamp
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# Write the timestamp to the log files
log.write(f"[{timestamp}] Log entry\n")
execution.write(f"[{timestamp}] Execution entry\n")

# Create a WebSocket connection        
ws_url = "wss://api-v2.upstox.com/feed/market-data-feed"  # Replace with the correct WebSocket URL
ws = WebSocket(api_key, access_token)
ws.connect(ws_url)
u.start_websocket(True)  # Start WebSocket connection with auto-reconnect

ws.on_connect = on_connect
ws.on_close = on_close
ws.on_error = on_error
ws.on_message = on_message

# Define event handlers
def on_connect(ws):
    # Subscribe to the desired symbols
    ws.subscribe([u.get_instrument_by_symbol('NSE_FO', script)], LiveFeedType.LTP)

def on_close(ws):
    # Handle WebSocket close event
    print("WebSocket connection closed")

def on_error(ws, error):
    # Handle WebSocket error event
    print("WebSocket error:", error)

def on_message(ws, message):
    # Handle WebSocket message event
    if message['type'] == 'ltp':
        ltp = message['data']['ltp']
        script = message['data']['symbol']
        print("Received LTP:", ltp)

        if is_profitable(script, ltp):
            print(f"{script} is profitable.")

        if is_loss(script, ltp):
            print(f"{script} is in a loss.")

        if is_trending_up(script, ltp):
            print(f"{script} is trending up.")

        buy(script, ltp)
        sell(script, ltp)
        # Perform any further processing or decision-making based on the received LTP
        # You can call your desired functions here, such as checking conditions and placing orders




def get_account_balance():
    balance = u.get_balance()
    return balance['equity']

account_balance = get_account_balance()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)