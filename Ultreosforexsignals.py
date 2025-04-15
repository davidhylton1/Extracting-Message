import re

def is_new_postion_ultreos_forex_signals(message):
    if ('SELL NOW' in message.upper() or 'BUY NOW' in message.upper()):
        return True
    else:
        return False
    

def extract_ultreos_forex_signals(msg):
    # Normalize message for easier parsing
    msg = msg.strip()
    msg = msg.replace(",", "")  # Remove commas from numeric values

    # Define patterns for the input format
    patterns = {
        "trade_pair": r"\b([A-Za-z0-9]+)\s+(buy|sell)\s+now",  # Matches "US500 sell now"
        "position_type": r"\b(buy|sell)\b",  # Matches "buy" or "sell"
        "open_price": r"\bnow\s*([\d.]+)",  # Matches the open price after "now"
        "tp": r"\btp\s*([\d.]+)",  # Matches all take-profit values
        "sl": r"\bsl\s*([\d.]+)"  # Matches the stop-loss value
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
    open_price = float(open_price_match.group(1)) if open_price_match else None

    # Extract TP (all take-profit values)
    tp_matches = re.findall(patterns["tp"], msg, re.IGNORECASE)
    tp = [float(tp) for tp in tp_matches] if tp_matches else []
    tp_first = tp[0] if tp else None

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

        if tp_first > 0:
            if position_type == 'SHORT':
                tp_percent = abs((open_price - tp_first) * 100 / open_price)
            else:
                tp_percent = abs((tp_first - open_price) * 100 / open_price)
        else:
            tp_percent = 0.5

    return trade_pair, position_type, open_price, tp_first, sl_percent, tp_percent
    
# Test cases
messages = [
    """US500 sell now 5650.9
sl 5798.4
tp 5504.0
tp 5406.2""",
    """USDJPY sell now 150.142
sl 152.097
tp 148.195
tp 146.990
tp 145.855""",
    """EURUSD buy now 1.08147
sl 1.07872
tp 1.08451
tp 1.08768""",
    """GBPNZD sell now 2.25365
sl 2.27505
tp 2.22934
tp 2.17100"""
]

for msg in messages:
    print(extract_ultreos_forex_signals(msg))
    print(is_new_postion_ultreos_forex_signals(msg))