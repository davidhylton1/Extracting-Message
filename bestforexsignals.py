import re

def is_new_postion_best_forex_signals(message):
    if ('TAKE PROFIT 1' in message.upper()):
        return True
    else:
        return False
    

def extract_best_forex_signals(msg):
    # Normalize message for easier parsing
    msg = msg.strip()
    msg = msg.replace(",", "")  # Remove commas from numeric values

    # Define patterns for the input format
    patterns = {
        "trade_pair": r"\b(BUY|SELL)\s*📈?📉?\s*([A-Za-z]{6})",  # Matches "BUY AUDUSD" or "SELL EURCAD" with optional emojis
        "position_type": r"\b(BUY|SELL)\b",  # Matches "BUY" or "SELL"
        "open_price": r"\(@\s*([\d.]+)\)",  # Matches the open price inside parentheses (@ 0.6354)
        "tp": r"Take profit \d+➡️at\s*([\d.]+)",  # Matches all take-profit values (TP1, TP2, TP3, etc.)
        "sl": r"Stop loss at\s*([\d.]+)"  # Matches the stop-loss value
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
    """🔵BUY 📈 AUDUSD (@ 0.6354)
Take profit 1➡️at  0.6381
Take profit 2➡️at  0.6428
Take profit 3➡️at  0.6479
Stop loss at  0.6295""",
    """🔵BUY 📈 CHFJPY (@ 170.33)
Take profit 1➡️at  170.68
Take profit 2➡️at  171.27
Take profit 3➡️at  171.88
Stop loss at  169.63""",
    """🔴SELL 📉GBPCAD (@ 1.8554) 
Take profit 1➡️at  1.8521
Take profit 2➡️at  1.8464
Take profit 3➡️at  1.8408
Stop loss at  1.8624""",
    """🔴SELL 📉EURCAD (@ 1.5609) 
Take profit 1➡️at  1.5575
Take profit 2➡️at  1.5520
Take profit 3➡️at  1.5466
Stop loss at  1.5679"""
]

for msg in messages:
    print(extract_best_forex_signals(msg))
    print(is_new_postion_best_forex_signals(msg))