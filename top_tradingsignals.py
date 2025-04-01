import re

def is_new_postion_anabel_signals(message):
    if ('BUY!' in message.upper() or 'SELL!' in message.upper()):
        return True
    else:
        return False
    

def extract_top_trading_signals(msg):
    # Normalize message for easier parsing
    msg = re.sub(r"\bENTER\b", "", msg, flags=re.IGNORECASE)
    msg = msg.strip()

    # Define patterns for the input format
    patterns = {
        "trade_pair": r"#([A-Za-z]+)",  # Matches the trade pair after '#'
        "position_type": r"\b(Buy|Sell)\b",  # Matches "Buy" or "Sell"
        "open_price": r"(?:support level|support|Support|resistance|Resistance|level|ahead)\s*(?:of|around)\s*([\d.]+)",  # Matches the support/resistance level (open price)
        "tp": r"Take\s*Profit\s*(?:of|at)\s*([\d.]+)",  # Matches the take-profit value
        "sl": r"Stop\s*Loss\s*(?:of|at)\s*([\d.]+)"  # Matches the stop-loss value
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
    """📉EUR-GBP Short From Resistance!

⭕Sell!
__
#EURGBP keeps growing
But the horizontal resistance
Is ahead around 0.8385
So after the retest will be
Expecting a local bearish
Correction to the downside
Sell!🔽
—
About Vip |WebSite |JoinVipNow
➖➖➖➖➖➖➖➖➖➖
⚡️
Consistent winnings 
⚡️
Tested strategy 
⚡️
Verified results 

🤩JOIN VIP SIGNALS NOW👇
@toptradingsignalsfx""",
    """📉AUD-NZD Local Correction Ahead!

⭕Sell!
__
#AUDNZD is already making
A pullback form a horizontal
Resistance of 1.1020 so we
Are locally bearish biased and
We will be expecting a further
Local bearish correction
Sell!🔽
—
About Vip |WebSite |JoinVipNow
➖➖➖➖➖➖➖➖➖➖
🤩JOIN VIP SIGNALS NOW👇
@toptradingsignalsfx""",
    """📈GBP-NZD Free Signal!

⭕Buy!
—
#GBPNZD is trading in an
Uptrend and the pair made
A bullish breakout of the
Key horizontal level of 2.2600
Which is now a support then
Made a retest and we are now
Seeing a bullish rebound
Already which reinforces our
Bullish bias on the pair and
Suggests that we enter
A long trade with the
Take Profit of 2.2715
And the Stop Loss of 2.2568
Buy!🔼
—
About Vip |WebSite |JoinVipNow
➖➖➖➖➖➖➖➖➖➖
🤩JOIN VIP SIGNALS NOW👇
@toptradingsignalsfx""",
    """📈EUR-CHF Potential Long!

⭕Buy!
—
#EURCHF is already making
A bullish rebound after the
Retest of the horizontal
Support of 0.9500 so we
Are locally bullish biased
And we will be expecting a
Further bullish move up
Buy!🔼
—
About Vip |WebSite |JoinVipNow
➖➖➖➖➖➖➖➖➖➖
🤩JOIN VIP SIGNALS NOW👇
@toptradingsignalsfx"""
]

for msg in messages:
    print(extract_top_trading_signals(msg))
    print(is_new_postion_anabel_signals(msg))