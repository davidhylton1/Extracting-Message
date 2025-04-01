import re

def extract_fx_signals(msg):
    # Normalize message for easier parsing
    msg = msg.strip()

    # Define patterns for the input format
    patterns = {
        "trade_pair": r"#([A-Za-z]+)",
        "position_type": r"\b(Buy|Long|Sell|Short)\b",  # Matches "Buy", "Long", "Sell", or "Short"
        "open_price": r"(?:Entry|Entry Point|Entry Level)\s*[-:]\s*([\d.]+)",  # Matches the entry price
        "tp": r"(?:Take|Take Profit|Tp)\s*[-:]\s*([\d.]+)",  # Matches the take-profit value
        "sl": r"(?:Stop|Stop Loss|Sl)\s*[-:]\s*([\d.]+)"  # Matches the stop-loss value
    }

    # Extract trade pair
    trade_pair_match = re.search(patterns["trade_pair"], msg, re.IGNORECASE)
    trade_pair = trade_pair_match.group(1).upper() if trade_pair_match else ""

    # Extract position type
    position_type_match = re.search(patterns["position_type"], msg, re.IGNORECASE)
    position_type = position_type_match.group(1).upper() if position_type_match else ""
    position_type = "LONG" if position_type in ["BUY", "LONG"] else "SHORT" if position_type in ["SELL", "SHORT"] else ""

    # Extract open price
    open_price_match = re.search(patterns["open_price"], msg, re.IGNORECASE)
    open_price = float(open_price_match.group(1)) if open_price_match else 0.0

    # Extract TP
    tp_match = re.search(patterns["tp"], msg, re.IGNORECASE)
    tp = float(tp_match.group(1)) if tp_match else 0.0

    # Extract SL
    sl_match = re.search(patterns["sl"], msg, re.IGNORECASE)
    sl = float(sl_match.group(1)) if sl_match else None

    # Return the extracted values
    return {
        "trade_pair": trade_pair,
        "position_type": position_type,
        "open_price": open_price,
        "tp": tp,
        "sl": sl
    }