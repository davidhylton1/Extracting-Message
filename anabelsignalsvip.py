import re

def is_new_postion_anabel_signals_vip(message):
    if ('SELL' in message.upper() or 'BUY' in message.upper()):
        return True
    else:
        return False
    

def extract_anabel_signals_vip(msg):
    # Normalize message for easier parsing
    msg = msg.strip()
    msg = msg.replace(",", "")  # Remove commas from numeric values

    # Define patterns for the input format
    patterns = {
        "trade_pair": r"\b([A-Za-z]+)\s+(BUY|SELL)",  # Matches "EURCHF BUY" or "EURCHF SELL"
        "position_type": r"\b(BUY|SELL)\b",  # Matches "BUY" or "SELL"
        "open_price": r"Entry\s*([\d.]+)",  # Matches the entry price after "Entry"
        "tp": r"Take\s*([\d.]+)",  # Matches the take-profit value after "Take"
        "sl": r"Stop\s*([\d.]+)"  # Matches the stop-loss value after "Stop"
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
    """EURCHF BUY🌸
——————
Entry 0.9275
Take  0.9387
 Stop 0.9214""",
    """GBPCAD SELL🌺
——————
Entry 1.8272
Take  1.7956
 Stop  1.8483""",
    """GBPJPY SELL🌺
——————
Entry 188.834
Take  184.689
 Stop  191.587""",
    """SILVER SELL🌺
——————
Entry 3,226.5
Take  3,034.5
 Stop  3,352.1"""
]

for msg in messages:
    print(extract_anabel_signals_vip(msg))
    print(is_new_postion_anabel_signals_vip(msg))