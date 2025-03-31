import re

def extract_anabel_signals(msg):
    # Normalize message for easier parsing
    msg = msg.strip()

    # Define patterns for the input format
    patterns = {
        "trade_pair": r"#([A-Za-z]+)",  # Matches the trade pair after '#'
        "position_type": r"\b(BUY|SELL)\b",  # Matches "BUY" or "SELL"
        "open_price": r"(?:level|psychological level|pivot level|trading on)\s*[-:]?\s*([\d.]+)",  # Matches the key level (open price)
        "tp": r"(Goal|Target)\s*[-:]\s*([\d.]+)",  # Matches the target price (TP)
        "sl": r"My Stop Loss\s*[-:]\s*([\d.]+)"  # Matches the stop-loss value (optional)
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
    sl = float(sl_match.group(1)) if sl_match and sl_match.group(1).replace('.', '', 1).isdigit() else None

    # Return the extracted values
    return {
        "trade_pair": trade_pair,
        "position_type": position_type,
        "open_price": open_price,
        "tp": tp,
        "sl": sl
    }
