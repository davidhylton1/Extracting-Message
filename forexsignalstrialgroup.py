import re

def is_new_postion_forex_signalstrial_group(message):
    if ('BUY!' in message.upper() or 'SELL!' in message.upper() or 'LONG!' in message.upper() or 'SHORT!' in message.upper()):
        return True
    else:
        return False
    
def extract_forex_signalstrial_group(msg):
    # Normalize message for easier parsing
    msg = msg.strip()
    msg = msg.replace(",", "")  # Remove commas from numeric values

    # Define patterns for the input format
    patterns = {
        "trade_pair": r"#([A-Za-z]+)|\b(GOLD|USOIL|WTI)\b",  # Matches the trade pair after "#" or specific keywords
        "position_type": r"\b(BUY|SELL|Bullish|Bearish|Long|Short)\b",  # Matches "BUY", "SELL", "Bullish", or "Bearish"
        "open_price": r"(?:testing a key support|trading on|pivot level|psychological level|key support|horizontal structure)\s*([\d.]+)",  # Matches the open price
        "tp": r"(?:movement at least to|bullish movement at least to|target|goal|achieve)\s*([\d.]+)",  # Matches the take-profit value
        "sl": r"(?:Recommended Stop Loss|Stop Loss)\s*[-:]\s*([\d.]+)"  # Matches the stop-loss value
    }

    # Extract trade pair
    trade_pair_match = re.search(patterns["trade_pair"], msg, re.IGNORECASE)
    trade_pair = trade_pair_match.group(1) or trade_pair_match.group(2) if trade_pair_match else ""
    trade_pair = trade_pair.upper()
    trade_pair = "XAUUSD" if trade_pair == "GOLD" else "WTI" if trade_pair == "USOIL" else trade_pair

    # Extract position type
    position_type_match = re.search(patterns["position_type"], msg, re.IGNORECASE)
    position_type = position_type_match.group(1).capitalize() if position_type_match else ""
    position_type = "LONG" if position_type in ["Buy", "Bullish", "Long"] else "SHORT" if position_type in ["Sell", "Bearish", "Short"] else ""

    # Extract open price
    open_price_match = re.search(patterns["open_price"], msg, re.IGNORECASE)
    open_price = float(open_price_match.group(1).strip(".")) if open_price_match else None  # Strip trailing period

    # Extract TP
    tp_match = re.search(patterns["tp"], msg, re.IGNORECASE)
    tp = float(tp_match.group(1).strip(".")) if tp_match else None  # Strip trailing period

    # Extract SL
    sl_match = re.search(patterns["sl"], msg, re.IGNORECASE)
    sl = float(sl_match.group(1).strip(".")) if sl_match else 0.5  # Strip trailing period

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

        if tp is not None and tp > 0:
            if position_type == 'SHORT':
                tp_percent = abs((open_price - tp) * 100 / open_price)
            else:
                tp_percent = abs((tp - open_price) * 100 / open_price)

    return trade_pair, position_type, open_price, sl, tp, sl_percent, tp_percent


# Test cases
messages = [
    """EURCHF My Opinion! BUY!

👩‍💻My dear friends,
EURCHF looks like it will make a good move, and here are the details:
The market is trading on 0.9524 pivot level.
Bias - Bullish
———————
Goal -0.9565
Recommended Stop Loss - 0.9499
————————
💐#EURCHF 
💹Time Frame : 7H (signal)
———————————
WISH YOU ALL LUCK🍀""",
    """🔅GOLD Will Go Up From Support! Long!📈
- - - - - - - - 
Please, check our technical outlook for 📊GOLD.

The price is testing a key support 3,024.22.

Current market trend & oversold RSI makes me think that buyers will push the price. I will anticipate a bullish movement at least to 3,056.10 level.""",
    """USOIL My Opinion! BUY!

👩‍💻My dear subscribers,
This is my opinion on the USOIL next move:
The instrument tests an important psychological level 68.97
Bias - Bullish

Target - 69.31
————————
💐#USOIL 
💹Time Frame :  1H (forecast)
———————————
WISH YOU ALL LUCK🍀""",
]

for msg in messages:
    print(extract_forex_signalstrial_group(msg))
    print(is_new_postion_forex_signalstrial_group(msg))