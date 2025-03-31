import re

def extract_free_signal_pro(msg):
    # Normalize message for easier parsing
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

    return {
        "trade_pair": trade_pair,
        "position_type": position_type,
        "open_price": open_price,
        "sl": sl,
        "tp": tp
    }
