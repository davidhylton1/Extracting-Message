import re

def is_new_postion_forex_gdp_signals(message):
    if ('FOREX SIGNAL' in message.upper()):
        return True
    else:
        return False
    
def extract_forex_gdp_signals(msg):
    # Normalize message for easier parsing
    msg = re.sub(r"\bENTER\b", "", msg, flags=re.IGNORECASE)
    msg = msg.strip()

    # Define patterns for the input format
    patterns = {
        "trade_pair": r"(?:Buy|Sell)\s+([A-Za-z]+)",  # Matches the trade pair after "Buy" or "Sell"
        "position_type": r"\b(Buy|Sell)\b",  # Matches "Buy" or "Sell"
        "open_price_range": r"at any price between\s*([\d.]+)\s*till\s*([\d.]+)",  # Matches the open price range
        "open_price_single": r"at\s*([\d.]+)",  # Matches a single open price
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

    # Extract open price
    open_price = None
    open_price_range_match = re.search(patterns["open_price_range"], msg, re.IGNORECASE)
    if open_price_range_match:
        # Calculate the average of the range
        open_price = (float(open_price_range_match.group(1)) + float(open_price_range_match.group(2))) / 2
    else:
        open_price_single_match = re.search(patterns["open_price_single"], msg, re.IGNORECASE)
        if open_price_single_match:
            open_price = float(open_price_single_match.group(1))

    # Extract TP (all targets)
    tp_matches = re.findall(patterns["tp"], msg, re.IGNORECASE)
    tp = [float(target) for target in tp_matches] if tp_matches else []
    tp = tp[0] if len(tp) > 1 else tp[0]

    # Extract SL
    sl_match = re.search(patterns["sl"], msg, re.IGNORECASE)
    sl = float(sl_match.group(1)) if sl_match else 0.5

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
    """🔼Forex Signal

Buy XAUUSD (Gold) at any price between 3019 till 3016

📊 Gold Analysis  

Gold has reached the higher low area of the Ascending triangle pattern

📊 How to trade triangle patterns? check here : https://www.forexgdp.com/learn/chart-patterns/#triangle

Target 1: 3025

Target 2: 3032

Target 3: 3040

Target 4: 3050

Stop Loss: 3009

Follow below signal rules

📍 After T1 reach, close some trade. Don't place any new trades. Move SL to Entry.

📍 If T1 is not hit Within 2 days (Signal day + Next Working Day AEDT time), If the trade is

at Entry = Close Trade
in Profit = Move SL to Entry
in Loss = Move TP to Entry

Take the 2-min quiz to handle signals better: https://www.forexgdp.com/follow/#quiz 

New to Signals? Read the rules here: https://www.forexgdp.com/follow/""",
    """🔽Forex Signal

Sell GBPNZD at any price between 2.2435 till 2.2460

📊 GBPNZD Analysis -GBPNZD is falling from the higher high area of the ascending channel and has started to move within a minor descending channel.

Target 1: 2.2388

Target 2: 2.2305

Target 3: 2.2210

Target 4: 2.2125

Stop Loss: 2.2522

Follow below signal rules

📍 After T1 reach, close some trade. Don't place any new trades. Move SL to Entry.

📍 If T1 is not hit Within 2 days (Signal day + Next Working Day AEDT time), If the trade is

at Entry = Close Trade
in Profit = Move SL to Entry
in Loss = Move TP to Entry

Take the 2-min quiz to handle signals better: https://www.forexgdp.com/follow/#quiz 

New to Signals? Read the rules here: https://www.forexgdp.com/follow/""",
    """🔽Forex Signal

Sell USDCAD at any price between 1.4312 till 1.4335

📊 USDCAD Analysis - USDCAD is falling from the historical resistance area. In the 4-hour timeframe, breaking the symmetrical triangle pattern

🔥 How to trade triangle breakouts? check here : https://www.forexgdp.com/learn/chart-patterns/#triangle

Target 1: 1.4265

Target 2: 1.4190

Target 3: 1.4107

Target 4: 1.4020

Stop Loss: 1.4398

Follow below signal rules

📍 After T1 reach, close some trade. Don't place any new trades. Move SL to Entry.

📍 If T1 is not hit Within 2 days (Signal day + Next Working Day AEDT time), If the trade is

at Entry = Close Trade
in Profit = Move SL to Entry
in Loss = Move TP to Entry

Take the 2-min quiz to handle signals better: https://www.forexgdp.com/follow/#quiz 

New to Signals? Read the rules here: https://www.forexgdp.com/follow/""",
    """📊 Forex Signal

Buy AUDUSD at any price between 0.6275 till 0.6250

AUDUSD Analysis - AUDUSD is rebounding from the major support area in the descending triangle on the weekly timeframe chart. On the 4-hour timeframe, AUDUSD has reached the higher low area of the ascending channel.

🔥 How to trade patterns in your chart? Check here : https://www.forexgdp.com/learn/chart-patterns/

Target 1: 0.6325

Target 2: 0.6390

Target 3: 0.6480

Stop Loss: 0.6187

Follow below signal rules

📍 After T1 reach, close some trade. Don't place any new trades. Move SL to Entry.

📍 If T1 is not hit Within 2 days (Signal day + Next Working Day AEDT time), If the trade is

at Entry = Close Trade
in Profit = Move SL to Entry
in Loss = Move TP to Entry

Take the 2-min quiz to handle signals better: https://www.forexgdp.com/follow/#quiz 

New to Signals? Read the rules here: https://www.forexgdp.com/follow/""",
    """🔽Forex Signal

Sell USDJPY at any price between 148.90 till 149.15

📊 USDJPY Analysis - USDJPY is falling from a lower high area of the descending channel after breaking and retesting the minor ascending channel line

Target 1: 148.42

Target 2: 147.60

Target 3: 146.80

Target 4: 145.75

Target 5: 144.25

Stop Loss: 149.78

Follow below signal rules

📍 After T1 reach, close some trade. Don't place any new trades. Move SL to Entry.

📍 If T1 is not hit Within 2 days (Signal day + Next Working Day AEDT time), If the trade is

at Entry = Close Trade
in Profit = Move SL to Entry
in Loss = Move TP to Entry

Take the 2-min quiz to handle signals better: https://www.forexgdp.com/follow/#quiz 

New to Signals? Read the rules here: https://www.forexgdp.com/follow/"""
]

for msg in messages:
    print(extract_forex_gdp_signals(msg))
    print(is_new_postion_forex_gdp_signals(msg))