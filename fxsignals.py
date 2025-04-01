import re

def is_new_postion_fx_signals(message):
    if ('LONG TRADE' in message.upper() or 'SHORT TRADE' in message.upper() or 'LONG TRADING' in message.upper() or 'SHORT TRADING' in message.upper()):
        return True
    else:
        return False
    
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
    """#GOLD: Long Trading Opportunity🔼

⭐️GOLD
- Classic bullish formation
- Our team expects pullback

⭐️SUGGESTED TRADE:

🔘
Swing Trade
🔴
Long GOLD
🔘
Entry - 3128.3
🟣
Sl - 3120.7
🟡
Tp - 3143.3
🔘
Our Risk - 1%

📈
 TradingView Link 
https://www.tradingview.com/chart/XAUUSD/JTnYCjdX-GOLD-Long-Trading-Opportunity/""",
    """#NZDJPY: Long Trade Explained🔼

⭐️NZDJPY
- Classic bullish pattern
- Our team expects retracement

⭐️SUGGESTED TRADE:

🔘
Swing Trade
🔴
Buy NZDJPY
🔘
Entry - 84.764
🟣
Stop - 84.140
🟡
Take - 85.960
🔘
Our Risk - 1%

📈
 TradingView Link 
https://www.tradingview.com/chart/NZDJPY/gbXLTrPq-NZDJPY-Long-Trade-Explained/""",
    """#AUDUSD: Long Trade with Entry/SL/TP🔼

⭐️AUDUSD
- Classic bullish setup
- Our team expects bullish continuation

⭐️SUGGESTED TRADE:

🔘
Swing Trade
🔴
Long AUDUSD
🔘
Entry Point - 0.6221
🟣
Stop Loss -  0.6186
🟡
Take Profit - 0.6287
🔘
Our Risk - 1%

📈
 TradingView Link 
https://www.tradingview.com/chart/AUDUSD/Qc2deFcQ-AUDUSD-Long-Trade-with-Entry-SL-TP/""",
    """#QQQ: Bullish Continuation & Long Trade🔼

⭐️QQQ
- Classic bullish formation
- Our team expects growth

⭐️SUGGESTED TRADE:

🔘
Swing Trade
🔴
Buy QQQ
🔘
Entry Level - 468.97
🟣
Sl - 457.71
🟡
Tp - 491.73
🔘
Our Risk - 1%

📈
 TradingView Link 
https://www.tradingview.com/chart/QQQ/fxJahaGz-QQQ-Bullish-Continuation-Long-Trade/""",
    """#SILVER: Short Trade with Entry/SL/TP🔽

⭐️SILVER
- Classic bearish setup
- Our team expects bearish continuation

⭐️SUGGESTED TRADE:

🔘
Swing Trade
🔴
Short SILVER
🔘
Entry Point - 34.116
🟣
Stop Loss - 34.505
🟡
Take Profit - 33.483
🔘
Our Risk - 1%

📈
 TradingView Link 
https://www.tradingview.com/chart/XAGUSD/madIUZwy-SILVER-Short-Trade-with-Entry-SL-TP/"""
]

for msg in messages:
    print(extract_fx_signals(msg))
    print(is_new_postion_fx_signals(msg))