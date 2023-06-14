from upstox_api.api import *
from upstox_api.exceptions import UpstoxException
from ratelimit import limits, RateLimitException, make_api_call
from datetime import datetime, time
import time as sleep
import os
import pandas as pd
from flask import Flask, request

app = Flask(__name__)

# Set up your Upstox API credentials

api_key = "api_key"
api_secret = "api_secret"
redirect_uri = "http://127.0.0.1"
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

    return "Access token retrieved successfully!"


u = Upstox(api_key, access_token)
ws = WebSocket(api_key, access_token)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

# Set the quantity for trading
quantity = 1
script = "NIFTY 18MAY23 18200 CE"

# Open log files
log = open("log.txt", "a")  # Open the file in append mode
execution = open("execution.txt", "a")  # Open the file in append mode
# Get the current timestamp
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# Write the timestamp to the log files
log.write(f"[{timestamp}] Log entry\n")
execution.write(f"[{timestamp}] Execution entry\n")



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

# Create a WebSocket connection        
ws_url = "wss://api.upstox.com/live/websocket"  # Replace with the correct WebSocket URL
ws.connect(ws_url)
u.start_websocket(True)  # Start WebSocket connection with auto-reconnect

ws.on_connect = on_connect
ws.on_close = on_close
ws.on_error = on_error
ws.on_message = on_message


def get_account_balance():
    balance = u.get_balance()
    return balance['equity']

account_balance = get_account_balance()


@limits(calls=10, period=1)  # Adjust the values as per Upstox API rate limits
def make_api_call(func, *args, **kwargs):
    return func(*args, **kwargs)


# @make_api_call
# def get_live_feed(script):
#     ltp = 0
#     try:
#         ltp = ws.get_live_feed(u.get_instrument_by_symbol('NSE_FO', script), LiveFeedType.LTP).get('ltp')

#     except UpstoxException as e:
#         print("Error fetching live feed:", e)
#     return ltp

@make_api_call
def get_ohlc_data(script):
    today = datetime.today().date()
    one_day_ago = today - pd.DateOffset(days=1)
    data = pd.DataFrame()
    try:
        data = pd.DataFrame(u.get_ohlc(u.get_instrument_by_symbol('NSE_FO', script), OHLCInterval.Minute_1, one_day_ago, today))
        data = data.set_index('timestamp')

    except UpstoxException as e:
        print(f"Error occurred while getting OHLC data for {script}: {str(e)}")
        log.write(f"Error occurred while getting OHLC data for {script}: {str(e)}")

    except RateLimitException as e:
        print(f"Rate limit exceeded. Waiting for {e.retry_after} seconds before retrying.")
        log.write(f"Rate limit exceeded. Waiting for {e.retry_after} seconds before retrying.")
        sleep.sleep(e.retry_after)

# Define the functions for checking conditions and placing orders
def is_profitable(script,ltp):
    try:
        position = pd.DataFrame(u.get_positions())
        if not position.empty:
            stock_position = position.loc[position["symbol"] == script]
            if not stock_position.empty:
                buy_price = stock_position["buy_price"].values[0]
                profit = ltp - buy_price
                if profit >= 4:
                    return True
    except UpstoxException as e:
        print(f"Error occurred while checking is_profitable for {script}: {str(e)}")
        log.write(f"Error occurred while checking is_profitable for {script}: {str(e)}")

    except RateLimitException as e:
        print(f"Rate limit exceeded. Waiting for {e.retry_after} seconds before retrying.")
        log.write(f"Rate limit exceeded. Waiting for {e.retry_after} seconds before retrying.")
        sleep.sleep(e.retry_after)

def is_loss(script,ltp):
    try:
        position = pd.DataFrame(u.get_positions())
        if not position.empty:
            stock_position = position.loc[position["symbol"] == script]
            if not stock_position.empty:
                buy_price = stock_position["buy_price"].values[0]
                loss = buy_price - ltp
                if loss >= 10:
                    return True
    except UpstoxException as e:
        print(f"Error occurred while checking is_loss for {script}: {str(e)}")
        log.write(f"Error occurred while checking is_loss for {script}: {str(e)}")

    except RateLimitException as e:
        print(f"Rate limit exceeded. Waiting for {e.retry_after} seconds before retrying.")
        log.write(f"Rate limit exceeded. Waiting for {e.retry_after} seconds before retrying.")
        sleep.sleep(e.retry_after)

def is_profitable_or_loss(script,ltp):
    try:
        if is_profitable(script,ltp):
            return "Profit"
        elif is_loss(script,ltp):
            return "Loss"
        else:
            return "No Profit/Loss"
    except UpstoxException as e:
        print(f"Error occurred while checking is_profitable_or_loss for {script}: {str(e)}")
        log.write(f"Error occurred while checking is_profitable_or_loss for {script}: {str(e)}")

    except RateLimitException as e:
        print(f"Rate limit exceeded. Waiting for {e.retry_after} seconds before retrying.")
        log.write(f"Rate limit exceeded. Waiting for {e.retry_after} seconds before retrying.")
        sleep.sleep(e.retry_after)


def is_trending_up(script,ltp):
    data = get_ohlc_data(script),
    data = data.tail(21) # Consider the last 21 candles for checking the closing price of the previous candle
    data["sma20"] = data.cp.rolling(window=20).mean().iloc[-2] # 20-day moving average of the previous candle
    data["psar"] = data.cp.shift(1).rolling(window=1).max().iloc[-2]  # PSAR with parameters (0.2, 0.2, 0.2) of the previous candle
    data["supertrend"] = data.cp.shift(1).rolling(window=9).min().iloc[-2] - 1.5 * data.tr.shift(1).rolling(window=9).std()  # Supertrend (9, 1.5) of the previous candle
    prev_closing = data.cp.iloc[-2]  # Closing price of the previous candle

    if ltp > data["sma20"].iloc[-1] and \
            data["cp"].iloc[-1] > data["psar"].iloc[-1] and \
            data["cp"].iloc[-1] > data["supertrend"].iloc[-1] and prev_closing > data["sma20"].iloc[-1] and \
            data["cp"].iloc[-1] > data["psar"].iloc[-1] and \
            data["cp"].iloc[-1] > data["supertrend"].iloc[-1]:
        return True
    return False

def is_rsi_between_30_and_70(script):
    data = get_ohlc_data(script)
    data = data.tail(14)
    data["change"] = data.cp.diff()
    data["gain"] = data.change.mask(data.change < 0, 0.0)
    data["loss"] = -data.change.mask(data.change > 0, -0.0)
    data["avg_gain"] = data.gain.ewm(com=13, adjust=False).mean()
    data["avg_loss"] = data.loss.ewm(com=13, adjust=False).mean()
    data["rs"] = data.avg_gain / data.avg_loss
    data["rsi"] = 100 - (100 / (1 + data.rs))
    rsi = data["rsi"].iloc[-1]
    if 30 <= rsi <= 70:
        return True
    return False


# Set the risk per trade as a percentage (e.g., 1%)
# risk_per_trade = 1

@make_api_call
def buy(script,ltp):
    try: 
        stop_loss = ltp - 10
        square_off = ltp + 4

        # Calculate the position size based on risk per trade and stop-loss price
        # position_size = int((risk_per_trade / 100) * account_balance / abs(ltp - stop_loss))

        # Place buy order
        order_id = u.place_order(TransactionType.Buy, u.get_instrument_by_symbol('NSE_FO', script),
                                 quantity, OrderType.Market, ProductType.Delivery, ltp, None, None, StopLossLimit(stop_loss))

        # Wait for the order to be executed
        while True:
            orders = pd.DataFrame(u.get_order_history())
            if not orders.empty:
                order = orders.loc[orders['order_id'] == order_id]
                if not order.empty:
                    status = order['status'].values[0]
                    if status == "COMPLETE":
                        execution.write("{} | Buy | {} | {} | {}\n".format(script, ltp, stop_loss, square_off))
                        return
            sleep.sleep(1)
    except UpstoxException as e:
        print(f"Error occurred while placing a buy order for {script}: {str(e)}")
        log.write(f"Error occurred while placing a buy order for {script}: {str(e)}")

    except RateLimitException as e:
        print(f"Rate limit exceeded. Waiting for {e.retry_after} seconds before retrying.")
        log.write(f"Rate limit exceeded. Waiting for {e.retry_after} seconds before retrying.")
        sleep.sleep(e.retry_after)

@make_api_call
def sell(script,ltp):
    try: 
        stop_loss = ltp + 10
        square_off = ltp - 4

        # Calculate the position size based on risk per trade and stop-loss price
        # position_size = int((risk_per_trade / 100) * account_balance / abs(ltp - stop_loss))

        # Place sell order
        order_id = u.place_order(TransactionType.Sell, u.get_instrument_by_symbol('NSE_FO', script),
                                 quantity, OrderType.Market, ProductType.Delivery, ltp, None, None, StopLossLimit(stop_loss))

        # Wait for the order to be executed
        while True:
            orders = pd.DataFrame(u.get_order_history())
            if not orders.empty:
                order = orders.loc[orders['order_id'] == order_id]
                if not order.empty:
                    status = order['status'].values[0]
                    if status == "COMPLETE":
                        execution.write("{} | Sell | {} | {} | {}\n".format(script, ltp, stop_loss, square_off))
                        return
            sleep.sleep(1)

    except UpstoxException as e:
        print(f"Error occurred while placing sell order for {script}: {str(e)}")
        log.write(f"Error occurred while placing a sell order for {script}: {str(e)}")

    except RateLimitException as e:
        print(f"Rate limit exceeded. Waiting for {e.retry_after} seconds before retrying.")
        log.write(f"Rate limit exceeded. Waiting for {e.retry_after} seconds before retrying.")
        sleep.sleep(e.retry_after)




@make_api_call       
def CheckTrades(script,ltp):
    try:
        run_trades = True  # Variable to control the loop
        buy_count = 0  # Track the number of buy trades
        sell_count = 0  # Track the number of sell trades
        trade_count = 0  # Track the total number of trades

        # Initialize a dictionary to keep track of bought scripts
        bought_scripts = {}

        # Function calls
        is_profitable(script,ltp)  # Pass the ltp value appropriately
        is_loss(script,ltp)  # Pass the ltp value appropriately
        is_trending_up(script,ltp)  # Pass the ltp value appropriately
        is_rsi_between_30_and_70(script,ltp)  # Pass the ltp value appropriately
        buy(script,ltp)
        sell(script,ltp)


        while run_trades and trade_count < 4:
            now = datetime.now()
            now_time = now.time()

            if (time(10, 21) <= now_time <= time(14, 15) and account_balance > 500):
                print("~~~~~~~~~~~~~~~~~~~~~~~ \nNow the time is: %s" % datetime.now().time())
                log.write("~~~~~~~~~~~~~~~~~~~~~~~ \nNow the time is: %s" % datetime.now().time())
                print("Checking for 20 min 5min MA Crossover for %s" % script)
                log.write("Checking for 20 min 5min MA Crossover for %s" % script)

                if is_trending_up(script) and is_rsi_between_30_and_70(script):
                    if script not in bought_scripts and buy_count < 2:
                        buy(script)
                        # Add the script to the bought_scripts dictionary
                        bought_scripts[script] = True
                        buy_count += 1
                        trade_count += 1
                    elif script in bought_scripts and is_profitable(script):
                        sell(script)
                        # Remove the script from the bought_scripts dictionary
                        del bought_scripts[script]
                        sell_count += 1
                        trade_count += 1
                    elif script in bought_scripts and is_loss(script):
                        sell(script)
                        # Remove the script from the bought_scripts dictionary
                        del bought_scripts[script]
                        sell_count += 1
                        trade_count += 1
        
                else:
                    print("Not meeting the buy or sell conditions for %s" % script)
                    log.write("Not meeting the buy or sell conditions for %s" % script)

            else:
                run_trades = False  # Break out of the loop if the condition is not met

        # Check if the maximum trade count has been reached
        if buy_count >= 2 and sell_count >= 2:
            run_trades = False  # Break out of the loop

    except RateLimitException as e:
        print(f"Rate limit exceeded. Waiting for {e.retry_after} seconds before retrying.")
        log.write(f"Rate limit exceeded. Waiting for {e.retry_after} seconds before retrying.")
        sleep.sleep(e.retry_after)
    except UpstoxException as e:
        print("An exception occurred while checking for check_trades:", str(e))
        log.write("An exception occurred while checking for check_trades: " + str(e))
        
while True:
    CheckTrades()
    print("\n***Now waiting for 60 seconds")
    log.write("\n***Now waiting for 60 seconds")
    sleep.sleep(60)

# Close the log files
log.close()
execution.close()




