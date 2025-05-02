import re

def is_new_postion_forex_signals_vip(message):
    if ('───────────────' in message.upper() or 'TP1' in message.upper()):
        return True
    else:
        return False
    

def extract_forex_signals_vip(msg):
    # Normalize message for easier parsing
    msg = msg.strip()
    msg = msg.replace(",", "")  # Remove commas from numeric values

    # Define patterns for the input format
    patterns = {
        "trade_pair": r"\b(Sell|Buy|Sell limit|Buy limit)\s+([A-Za-z0-9]+)",  # Matches "Sell limit GBPNZD" or "Buy limit US30"
        "position_type": r"\b(Sell|Buy|Sell limit|Buy limit)\b",  # Matches "Sell", "Buy", "Sell limit", or "Buy limit"
        "entry_price": r"(?:My entry|at|NOW)\s*([\d.]+)",  # Matches the entry price after "My entry", "at", or "NOW"
        "tp": r"TP\d[:\s]*([\d.]+)|Take Profit\s*([\d.]+)",  # Matches all take-profit levels (e.g., TP1, TP2, TP3) or "Take Profit"
        "sl": r"(?:SL|Stop Loss)[:\s]*([\d.]+)"  # Matches the stop-loss value
    }

    # Extract trade pair
    trade_pair_match = re.search(patterns["trade_pair"], msg, re.IGNORECASE)
    trade_pair = trade_pair_match.group(2).upper() if trade_pair_match else ""

    # Extract position type
    position_type_match = re.search(patterns["position_type"], msg, re.IGNORECASE)
    position_type = position_type_match.group(1).upper() if position_type_match else ""
    position_type = "LONG" if "BUY" in position_type else "SHORT" if "SELL" in position_type else ""

    # Extract entry price
    entry_price_match = re.search(patterns["entry_price"], msg, re.IGNORECASE)
    open_price = float(entry_price_match.group(1)) if entry_price_match else None

    # Extract TP (all take-profit values)
    tp_matches = re.findall(patterns["tp"], msg, re.IGNORECASE)
    tp = [float(tp[0] or tp[1]) for tp in tp_matches if tp[0] or tp[1]]  # Handle both TP1/TP2/TP3 and "Take Profit"

    # Use the first TP value if available
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
    """Buy limit USDJPY

My entry  139.90
SL 138.90
TP1 140.10
TP2 140.40
TP3 140.90

I'm risking 0.5% use appropriate risk management.

""",
    """1. 24/03/25 
───────────────
📉BUY CADCHF at 0.61540
Stop Loss 0.61120
Take Profit 0.62540
APPROPRIATE LOT SIZE 1% risk
Risk/ Reward 1:2.5
───────────────""",
    """Buy GOLD NOW 3306
Tp1: 3310
Tp2: 3314
Tp3: 3326
Sl: 3300
Apply proper risk"""
,
    """Sell limit GBPNZD

My entry  2.23800
SL 2.24800
TP1 2.23600
TP2 2.23400
TP3 2.22800

I'm risking 0.5% use appropriate risk management.

"""
]

for msg in messages:
    print(extract_forex_signals_vip(msg))
    print(is_new_postion_forex_signals_vip(msg))