import re

def is_new_postion_forex_signals_vipx2(message):
    if ('BUY' in message.upper() or 'SELL' in message.upper()):
        return True
    else:
        return False
    

def extract_forex_signals_vipx2(msg):
    # Normalize message for easier parsing
    msg = msg.strip()
    msg = msg.replace(",", "")  # Remove commas from numeric values

    # Define patterns for the input format
    patterns = {
        "trade_pair": r"\b(XAUUSD)\b",  # Matches the trade pair "XAUUSD"
        "position_type": r"\b(Buy|Sell)\b",  # Matches "Buy" or "Sell"
        "open_price": r"\b(Sell|Buy)\s*([\d.]+)",  # Matches the open price after "Sell" or "Buy"
        "tp": r"💰TP\d+\s*([\d.]+)",  # Matches all take-profit values (TP1, TP2, TP3, etc.)
        "sl": r"🚫SL\s*([\d.]+)"  # Matches the stop-loss value
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

    # Extract TP (all take-profit values)
    tp_matches = re.findall(patterns["tp"], msg, re.IGNORECASE)
    tp = [float(tp) for tp in tp_matches] if tp_matches else []

    # Use the first TP value if available
    tp_first = tp[0] if tp else None

    # Extract SL
    sl_match = re.search(patterns["sl"], msg, re.IGNORECASE)
    sl = float(sl_match.group(1)) if sl_match else None

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

        if tp_first > 0:
            if position_type == 'SHORT':
                tp_percent = abs((open_price - tp_first) * 100 / open_price)
            else:
                tp_percent = abs((tp_first - open_price) * 100 / open_price)
        else:
            tp_percent = 0.5

        return trade_pair, position_type, open_price, sl, tp_first, sl_percent, tp_percent
    
# Test cases
messages = [
    """XAUUSD 📉 SELL 2925.00

💰TP1 2923.00
💰TP2 2920.00
💰TP3 2915.00
🚫SL 2933.50

ForexSignals.io content""",
    """XAUUSD 📉 SELL 2950.00

💰TP1 2948.00
💰TP2 2945.00
💰TP3 2940.00
🚫SL 2958.50

ForexSignals.io content""",
    """XAUUSD 📈 BUY 3105.50

💰TP1 3107.50
💰TP2 3110.50
💰TP3 3115.50
🚫SL 3097.00

ForexSignals.io content""",
    """XAUUSD 📉 SELL 3130.00

💰TP1 3128.00
💰TP2 3125.00
💰TP3 3120.00
🚫SL 3138.50

ForexSignals.io content"""
]

for msg in messages:
    print(extract_forex_signals_vipx2(msg))
    print(is_new_postion_forex_signals_vipx2(msg))