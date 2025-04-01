import re

def is_new_postion_signal_provider(message):
    if ('BUY!' in message.upper() or 'SELL!' in message.upper() or 'SHORT!' in message.upper() or 'LONG!' in message.upper()):
        return True
    else:
        return False
    
def extract_signal_provider(msg):
    # Normalize message for easier parsing
    msg = re.sub(r"\bENTER\b", "", msg, flags=re.IGNORECASE)
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
    """🔅EURUSD Is Very Bullish! Buy!📈
- - - - - - - - 
Here is our detailed technical review for 📊EURUSD.

The market is approaching a significant support area 1.079.

The underlined horizontal cluster clearly indicates a highly probable bullish movement with target 1.109 level.
- - - - - - - - 
#freesignal #eurusd
- - - - - - - -
🌐About VIP: signalprovider.org
❓FAQ: signalprovider.org/faq
📲: @signalprovidercontact""",
    """🔅USOIL Is Bullish! Long!📈
- - - - - - - - 
Please, check our technical outlook for 📊USOIL.

The market is approaching a key horizontal level 71.913.

Considering the today's price action, probabilities will be high to see a movement to 73.911.
- - - - - - - - 
#freesignal #usoil
- - - - - - - -
🌐About VIP: signalprovider.org
❓FAQ: signalprovider.org/faq
📲: @signalprovidercontact""",
    """📈NZDCAD Will Fall! Sell!🔻
- - - - - - - - 
Please, check our technical outlook for❗NZDCAD.

The price is testing a key resistance 0.816.

Taking into consideration the current market trend & overbought RSI, chances will be high to see a bearish movement to the downside at least to 0.813 level.
- - - - - - - - 
#freeforecast #nzdcad
- - - - - - - -
🌐About VIP: signalprovider.org
❓FAQ: signalprovider.org/faq
📲: @signalprovidercontact""",
    """📈GBPJPY Is Going Down! Short!🔻
- - - - - - - - 
Take a look at our analysis for❗GBPJPY.

The market is on a crucial zone of supply 193.030.

The above-mentioned technicals clearly indicate the dominance of sellers on the market. I recommend shorting the instrument, aiming at 192.202 level.
- - - - - - - - 
#freeforecast #gbpjpy
- - - - - - - -
🌐About VIP: signalprovider.org
❓FAQ: signalprovider.org/faq
📲: @signalprovidercontact""",
    """📈GBPUSD Will Go Up! Buy!🟢
- - - - - - - - 
Please, check our technical outlook for 🟢GBPUSD.

The market is approaching a key horizontal level 1.294.

Considering the today's price action, probabilities will be high to see a movement to 1.305.
- - - - - - - - 
#freeforecast #gbpusd
- - - - - - - -
⭐️ Key Benefits of VIP Group:

⭐️ 3-4 Exclusive Daily Signals 
⭐️ One Take Profit  
⭐️ Stop Loss
⭐️ High Accuracy  
⭐️ Minimal risk  

JOIN NOW via Bot: 
@signalprovidervipbot
CONTACT: 
@signalprovidercontact"""
]

for msg in messages:
    print(extract_signal_provider(msg))
    print(is_new_postion_signal_provider(msg))