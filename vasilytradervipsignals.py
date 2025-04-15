import re

def is_new_postion_vasily_trading_signals(message):
    if ('LONG FROM' in message.upper() or 'SELL FROM' in message.upper()):
        return True
    else:
        return False
    

def extract_vasily_trading_signals(msg):
    # Normalize message for easier parsing
    msg = msg.strip()
    msg = msg.replace(",", "")  # Remove commas from numeric values

    # Define patterns for the input format
    patterns = {
        "trade_pair": r"\b([A-Za-z]{6})\b",  # Matches the trade pair (e.g., "GBPJPY")
        "position_type": r"\b(Long|Short)\b",  # Matches "Long" or "Short"
        "open_price": r"\b(Long|Short)\s*From\s*([\d.]+)",  # Matches the open price after "Long From" or "Short From"
        "tp": r"Take Profit[:\s]*([\d.]+)",  # Matches the take-profit value
        "sl": r"Stop Loss[:\s]*([\d.]+)"  # Matches the stop-loss value
    }

    # Extract trade pair
    trade_pair_match = re.search(patterns["trade_pair"], msg, re.IGNORECASE)
    trade_pair = trade_pair_match.group(1).upper() if trade_pair_match else ""

    # Extract position type
    position_type_match = re.search(patterns["position_type"], msg, re.IGNORECASE)
    position_type = position_type_match.group(1).upper() if position_type_match else ""
    position_type = "LONG" if position_type == "LONG" else "SHORT" if position_type == "SHORT" else ""

    # Extract open price
    open_price_match = re.search(patterns["open_price"], msg, re.IGNORECASE)
    open_price = float(open_price_match.group(2)) if open_price_match else None

    # Extract TP
    tp_match = re.search(patterns["tp"], msg, re.IGNORECASE)
    tp = float(tp_match.group(1)) if tp_match else None

    # Extract SL
    sl_match = re.search(patterns["sl"], msg, re.IGNORECASE)
    sl = float(sl_match.group(1)) if sl_match else 0.5

    # Normalize trade pair and position type
    trade_pair = 'XAUUSD' if trade_pair.upper() == 'GOLD' else trade_pair.upper()

    # Initialize percentages
    sl_percent = None
    tp_percent = None

    # Calculate percentages if possible
    if open_price > 0:  # Ensure open_price is valid
        if sl is not None:
            if position_type == 'SHORT':
                sl_percent = abs((sl - open_price) * 100 / open_price)
            else:
                sl_percent = abs((open_price - sl) * 100 / open_price)
        else:
            sl_percent = 0.5

        if tp > 0:
            if position_type == 'SHORT':
                tp_percent = abs((open_price - tp) * 100 / open_price)
            else:
                tp_percent = abs((tp - open_price) * 100 / open_price)
        else:
            tp_percent = 0.5

    return trade_pair, position_type, open_price, sl, tp, sl_percent, tp_percent
    
# Test cases
messages = [
    """NZDUSD Long From 0.5717
Take Profit: 0.57318
Stop Loss: 0.57092""",
    """CHFJPY Short From 169.37
Take Profit: 168.773
Stop Loss: 169.89""",
    """CADJPY Short From 105.42
Take Profit: 105.06
Stop Loss: 105.7""",
    """NZDUSD Long From 0.57445
Take Profit: 0.5776
Stop Loss: 0.57206"""
]

for msg in messages:
    print(extract_vasily_trading_signals(msg))
    print(is_new_postion_vasily_trading_signals(msg))