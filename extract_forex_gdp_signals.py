import re

def extract_forex_gdp_signals(msg):
    # Normalize message for easier parsing
    msg = msg.strip()

    # Define patterns for the input format
    patterns = {
        "trade_pair": r"(?:Buy|Sell)\s+([A-Za-z]+)",  # Matches the trade pair after "Buy" or "Sell"
        "position_type": r"\b(Buy|Sell)\b",  # Matches "Buy" or "Sell"
        "open_price_range": r"at any price between\s*([\d.]+)\s*till\s*([\d.]+)",  # Matches the open price range
        "tp": r"Target\s*\d+:\s*([\d.]+)",  # Matches all target prices
        "sl": r"Stop Loss:\s*([\d.]+)"  # Matches the stop-loss value
    }

    # Extract trade pair
    trade_pair_match = re.search(patterns["trade_pair"], msg, re.IGNORECASE)
    trade_pair = trade_pair_match.group(1).upper() if trade_pair_match else ""

    # Extract position type
    position_type_match = re.search(patterns["position_type"], msg, re.IGNORECASE)
    position_type = position_type_match.group(1).upper() if position_type_match else ""
    position_type = "LONG" if position_type == "BUY" else "SHORT" if position_type == "SELL" else ""

    # Extract open price range
    open_price_range_match = re.search(patterns["open_price_range"], msg, re.IGNORECASE)
    open_price_range = f"{open_price_range_match.group(1)} - {open_price_range_match.group(2)}" if open_price_range_match else ""

    # Extract TP (all targets)
    tp_matches = re.findall(patterns["tp"], msg, re.IGNORECASE)
    tp = [float(target) for target in tp_matches] if tp_matches else []

    # Extract SL
    sl_match = re.search(patterns["sl"], msg, re.IGNORECASE)
    sl = float(sl_match.group(1)) if sl_match else None

    # Return the extracted values
    return {
        "trade_pair": trade_pair,
        "position_type": position_type,
        "open_price_range": open_price_range,
        "tp": tp,
        "sl": sl
    }