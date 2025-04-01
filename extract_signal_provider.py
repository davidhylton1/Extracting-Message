import re

def extract_signal_provider(msg):
    # Normalize message for easier parsing
    msg = msg.strip()

    # Define patterns for the input format
    patterns = {
        "trade_pair": r"#([A-Za-z]+)",  # Matches all hashtags
        "position_type": r"\b(Long|Buy|Short|Sell)\b",  # Matches "Long", "Buy", "Short", or "Sell"
        "open_price": r"(?:horizontal structure|resistance area|key support|support area|zone of supply|horizontal level|key resistance|of demand)\s*([\d.,]+)\b",  # Matches the key support or horizontal structure (open price)
        "tp": r"(?:achieve|movement to|target|at least to|will reach|with goal|down to|aiming at)\s*([\d.,]+)\b",  # Matches the take-profit level
        "sl": r"Stop Loss\s*[-:]\s*([\d.,]+)\b"  # Matches the stop-loss value (if provided)
    }

    # Extract all trade pairs (hashtags)
    trade_pair_matches = re.findall(patterns["trade_pair"], msg, re.IGNORECASE)
    trade_pair = trade_pair_matches[1].upper() if len(trade_pair_matches) > 1 else ""  # Select the second hashtag

    # Extract position type
    position_type_match = re.search(patterns["position_type"], msg, re.IGNORECASE)
    position_type = position_type_match.group(1).upper() if position_type_match else ""
    position_type = "LONG" if position_type in ["BUY", "LONG"] else "SHORT" if position_type in ["SELL", "SHORT"] else ""

    # Extract open price
    open_price_match = re.search(patterns["open_price"], msg, re.IGNORECASE)
    open_price = float(open_price_match.group(1).replace(",", "")) if open_price_match else 0.0

    # Extract TP
    tp_match = re.search(patterns["tp"], msg, re.IGNORECASE)
    tp = float(tp_match.group(1).replace(",", "")) if tp_match else 0.0

    # Extract SL
    sl_match = re.search(patterns["sl"], msg, re.IGNORECASE)
    sl = float(sl_match.group(1).replace(",", "")) if sl_match else None

    # Return the extracted values
    return {
        "trade_pair": trade_pair,
        "position_type": position_type,
        "open_price": open_price,
        "tp": tp,
        "sl": sl
    }