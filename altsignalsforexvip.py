import re

def is_new_postion_alt_signals_forex_vip(message):
    if ('───────────────' in message.upper()):
        return True
    else:
        return False
    

def extract_alt_signals_forex_vip(msg):
    # Normalize message for easier parsing
    msg = msg.strip()
    msg = msg.replace(",", "")  # Remove commas from numeric values

    # Define patterns for the input format
    patterns = {
        "trade_pair": r"\b(BUY|SELL)\s+([A-Za-z0-9]+)",  # Matches "BUY US30" or "SELL XAUUSD"
        "position_type": r"\b(Buy|Sell)\b",  # Matches "Buy" or "Sell"
        "open_price": r"\b(Buy|Sell)\s+[A-Za-z0-9]+\s+at\s+([\d.]+)",  # Matches the open price after "Buy/Sell ... at"
        "tp": r"Take Profit\s*([\d.]+)",  # Matches the take-profit value
        "sl": r"Stop Loss\s*([\d.]+)"  # Matches the stop-loss value
    }

    # Extract trade pair
    trade_pair_match = re.search(patterns["trade_pair"], msg, re.IGNORECASE)
    trade_pair = trade_pair_match.group(2).upper() if trade_pair_match else ""

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
    if open_price is not None and open_price > 0:  # Ensure open_price is valid
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
    """1. 02/04/25 
───────────────
📉BUY US30 at 42000
Stop Loss 41750
Take Profit 43000
APPROPRIATE LOT SIZE 1% risk
Risk/ Reward 1:4
───────────────""",
    """1. 01/04/25 
───────────────
📉BUY USTEC at 19250
Stop Loss 19000
Take Profit 20000
APPROPRIATE LOT SIZE 1% risk
Risk/ Reward 1:4
───────────────""",
    """1. 31/03/25 
───────────────
📉BUY AUDCAD at 0.89760
Stop Loss 0.89300
Take Profit 0.92000
APPROPRIATE LOT SIZE 1% risk
Risk/ Reward 1:3
───────────────""",
    """1. 24/03/25 
───────────────
📉BUY CADCHF at 0.61540
Stop Loss 0.61120
Take Profit 0.62540
APPROPRIATE LOT SIZE 1% risk
Risk/ Reward 1:2.5
───────────────"""
]

for msg in messages:
    print(extract_alt_signals_forex_vip(msg))
    print(is_new_postion_alt_signals_forex_vip(msg))