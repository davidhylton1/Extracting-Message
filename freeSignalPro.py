import re

def is_new_postion_free_signal_pro_signal(message):
    if ('BUY' in message.upper() or 'SELL' in message.upper()) and ('@' in message or ' AT ' in message.upper()):
        return True
    else:
        return False

def extract_free_signal_pro(msg):
    # Normalize message for easier parsing
    msg = re.sub(r"\bENTER\b", "", msg, flags=re.IGNORECASE)
    msg = msg.strip()

    # Position type (Buy/Sell)
    position_type_match = re.search(r"\b(Buy|Sell)\b", msg, re.IGNORECASE)
    position_type = position_type_match.group(1).capitalize() if position_type_match else ""

    # Trade pair: get word before or after Buy/Sell
    trade_pair = ""
    if position_type:
        pattern_before = rf"([A-Za-z]+)\s+{position_type}"
        pattern_after = rf"{position_type}\s+([A-Za-z]+)"
        match_before = re.search(pattern_before, msg, re.IGNORECASE)
        match_after = re.search(pattern_after, msg, re.IGNORECASE)
        if match_before:
            trade_pair = match_before.group(1).upper()
        elif match_after:
            trade_pair = match_after.group(1).upper()

    # Open price: range or single
    open_price_match = re.search(r"@\s*([\d.]+)\s*-\s*([\d.]+)", msg)
    if open_price_match:
        open_price = [float(open_price_match.group(1)), float(open_price_match.group(2))]
    else:
        single_price_match = re.search(r"\b(?:at|@)\s*([\d.]+)", msg)
        open_price = [float(single_price_match.group(1))] if single_price_match else []

    # SL
    sl_match = re.search(r"\bSL\s*[-:]?\s*([\d.]+)", msg, re.IGNORECASE)
    sl = float(sl_match.group(1)) if sl_match else 0.0

    # TP values
    tp_matches = re.findall(r"\bTP\d*\s*[-:]?\s*([\d.]+)", msg, re.IGNORECASE)
    tp = [float(val) for val in tp_matches]

    position_type = 'LONG' if position_type.upper() == 'BUY' else 'SHORT' if position_type.upper() == 'SELL' else position_type
    trade_pair = 'XAUUSD' if trade_pair.upper() == 'GOLD' else trade_pair.upper()
    
    open_price = open_price[0] if len(open_price) > 1 else open_price[0]
    stop_loss = sl
    take_profit = tp[0] if len(tp) > 1 else tp[0]

    if position_type == 'SHORT':
        sl_percent = abs((stop_loss - open_price)*100/open_price)
        tp_percent = abs((open_price - take_profit)*100/open_price)
    else:
        sl_percent = abs((open_price - stop_loss)*100/open_price)
        tp_percent = abs((take_profit - open_price)*100/open_price)

    return trade_pair, position_type, open_price, stop_loss, take_profit, sl_percent, tp_percent

# Test cases
messages = [
    """Sell nzdjpy at 75.820
Sl : 76.320
Tp1 : 75.320
Tp2 : 74.820""",
    """Gold sell @1795 - 1798

SL 1803

TP 1792
TP 1790
TP 1786""",
    """Sell usdjpy at 109. 700
Sl : 110. 100
Tp1 : 109.300
Tp2 : 108.900""",
    """Sell eurcad at 1.53630
Sl - 1.53930
Tp1 - 1.53230
Tp2 - 1.52830""",
    """Gold buy @1772.5-1770

SL 1767

TP 1775
TP 1779
TP open"""
]

for msg in messages:
    print(extract_free_signal_pro(msg))
    print(is_new_postion_free_signal_pro_signal(msg))