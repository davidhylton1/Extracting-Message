import re

def is_new_postion_anabel_signals(message):
    if ('BUY!' in message.upper() or 'SELL!' in message.upper()):
        return True
    else:
        return False
    
def extract_anabel_signals(msg):
    # Normalize message for easier parsing
    msg = re.sub(r"\bENTER\b", "", msg, flags=re.IGNORECASE)
    msg = msg.strip()

    # Define patterns for the input format
    patterns = {
        "trade_pair": r"#([A-Za-z]+)",  # Matches the trade pair after '#'
        "position_type": r"\b(BUY|SELL)\b",  # Matches "BUY" or "SELL"
        "open_price": r"(?:level|psychological level|pivot level|pivot point|trading on)\s*[-:]?\s*([\d.]+)",  # Matches the key level (open price)
        "tp": r"(Goal|Target)\s*[-:]\s*([\d.]+)",  # Matches the target price (TP)
        "sl": r"Stop Loss\s*[-:]\s*([\d.]+)"  # Matches the stop-loss value (optional)
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
    open_price = float(open_price_match.group(1)) if open_price_match and open_price_match.group(1).replace('.', '', 1).isdigit() else 0.0

    # Extract TP
    tp_match = re.search(patterns["tp"], msg, re.IGNORECASE)
    tp = float(tp_match.group(2)) if tp_match and tp_match.group(2).replace('.', '', 1).isdigit() else 0.0

    # Extract SL (optional)
    sl_match = re.search(patterns["sl"], msg, re.IGNORECASE)
    sl = float(sl_match.group(1)) if sl_match and sl_match.group(1).replace('.', '', 1).isdigit() else 0.5

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

        if tp > 0:
            if position_type == 'SHORT':
                tp_percent = abs((open_price - tp) * 100 / open_price)
            else:
                tp_percent = abs((tp - open_price) * 100 / open_price)

    return trade_pair, position_type, open_price, sl, tp, sl_percent, tp_percent
# Test cases
messages = [
    """GBPCAD Set To Fall! SELL!

👩‍💻My dear subscribers,
My technical analysis for GBPCAD is below:
The price is coiling around a solid key level - 1.8578
Bias - Bearish

Goal - 1.8493
————————
💐#GBPCAD 
💹Time Frame :  5H (forecast)
———————————
WISH YOU ALL LUCK🍀

""",
    """NZDUSD Technical Analysis! BUY!

👩‍💻My dear subscribers,
This is my opinion on the NZDUSD next move:
The instrument tests an important psychological level 0.5666
Bias - Bullish
———————
Target - 0.5722
My Stop Loss - 0.5632
————————
💐#NZDUSD 
💹Time Frame : 12H (signal)
———————————
WISH YOU ALL LUCK🍀

""",
    """EURUSD Massive Long! BUY!

👩‍💻My dear friends,
Please, find my technical outlook for EURUSD below:
The instrument tests an important psychological level 1.0795
Bias - Bullish

Target - 1.0810
————————
💐#EURUSD 
💹Time Frame :  1H (forecast)
———————————
WISH YOU ALL LUCK🍀

""",
    """USDJPY Set To Grow! BUY!

👩‍💻My dear followers,
This is my opinion on the USDJPY next move:
The asset is approaching an important pivot point 149.16
Bias - Bullish

Goal - 150.13
————————
💐#USDJPY 
💹Time Frame :  5H (forecast)
———————————
WISH YOU ALL LUCK🍀"""
]

for msg in messages:
    print(extract_anabel_signals(msg))
    print(is_new_postion_anabel_signals(msg))