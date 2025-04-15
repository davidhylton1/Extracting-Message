import re

def is_new_postion_top_trading_signals_pro(message):
    if ('BUY' in message.upper() or 'SELL' in message.upper()):
        return True
    else:
        return False
    

def extract_top_trading_signals_pro(msg):
    # Normalize message for easier parsing
    msg = msg.strip()
    msg = msg.replace(",", "")  # Remove commas from numeric values

    # Define patterns for the input format
    patterns = {
        "trade_pair": r"\b([A-Za-z]{6})\b",  # Matches the trade pair (e.g., "Eurusd")
        "position_type": r"\b(Buy|Sell)\b",  # Matches "Buy" or "Sell"
        "open_price": r"\b(Sell|Buy)\s*([\d.]+)",  # Matches the open price after "Sell" or "Buy"
        "tp": r"\bTp\s*([\d.]+)",  # Matches the take-profit value
        "sl": r"\bSl\s*([\d.]+)"  # Matches the stop-loss value
    }

    # Extract trade pair
    trade_pair_match = re.search(patterns["trade_pair"], msg, re.IGNORECASE)
    trade_pair = trade_pair_match.group(1).upper() if trade_pair_match else ""

    # Extract position type
    position_type_match = re.search(patterns["position_type"], msg, re.IGNORECASE)
    position_type = position_type_match.group(1).upper() if position_type_match else ""
    position_type = "LONG" if position_type == "BUY" else "SHORT" if position_type == "SELL" else ""

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
    """Eurusd sell 1.0804
Tp 1.0784
Sl 1.0810""",
    """Usdcad sell 1.4378
Tp 1.4300
Sl 1.4412""",
    """Nzdjpy buy 84.837
Tp 85.976
Sl 84.446""",
    """Audusd buy 0.6230
Tp 0.6294
Sl 0.6197"""
]

for msg in messages:
    print(extract_top_trading_signals_pro(msg))
    print(is_new_postion_top_trading_signals_pro(msg))