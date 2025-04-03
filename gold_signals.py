import re

def is_new_postion_gold_signals(message):
    if ('SIGNAL DETAILS' in message.upper()):
        return True
    else:
        return False
    
def extract_gold_signals(msg):
    # Normalize message for easier parsing
    msg = msg.strip()
    msg = msg.replace(",", "")  # Remove commas from numeric values

    # Define patterns for the input format
    patterns = {
        "trade_pair": r"📊([A-Za-z]+):",  # Matches the trade pair after "📊"
        "position_type": r"\b(Buy|Sell)\b",  # Matches "Buy" or "Sell"
        "open_price": r"CURRENT PRICE:\s*([\d.]+)",  # Matches the current price
        "sl": r"STOP LOSS:\s*([\d.]+)",  # Matches the stop-loss value
        "tp": r"TAKE PROFIT:\s*([\d.]+)"  # Matches the take-profit value
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

    # Extract SL
    sl_match = re.search(patterns["sl"], msg, re.IGNORECASE)
    sl = float(sl_match.group(1)) if sl_match else 0.5

    # Extract TP
    tp_match = re.search(patterns["tp"], msg, re.IGNORECASE)
    tp = float(tp_match.group(1)) if tp_match else 0.0

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
    """📊DXY: Local Correction Ahead! Buy!

🆓SIGNAL DETAILS 
——————
ENTER: Long trade 
CURRENT PRICE: 104.288
STOP LOSS:    104.185
TAKE PROFIT: 104.439
——————
🔔SUGGESTED RISK:
1% of the account for each trade

👑Wish you good luck in trading to you all!
——————
✈️ CONTACT TO JOIN GOLD SIGNALS VIP👉🏻 @goldvip_contact

😍 OR JOIN VIP IN BOT👉🏻@GoldSignalsVipPaymentBot""",
    """📊SILVER: Market Is Looking Up! Buy!

🆓SIGNAL DETAILS 
——————
ENTER: Long trade 
CURRENT PRICE:  33.84301
STOP LOSS:    33.68869
TAKE PROFIT: 34.07705
——————
🔔SUGGESTED RISK:
1% of the account for each trade

👑Wish you good luck in trading to you all!
——————
✈️ CONTACT TO JOIN GOLD SIGNALS VIP👉🏻 @goldvip_contact

😍 OR JOIN VIP IN BOT👉🏻@GoldSignalsVipPaymentBot""",
    """📊GOLD: Growth Is Coming! Buy!

🆓SIGNAL DETAILS 
——————
ENTER: Long trade 
CURRENT PRICE:  3,132.90
STOP LOSS:    3,123.79
TAKE PROFIT: 3,146.75
——————
🔔SUGGESTED RISK:
1% of the account for each trade

👑Wish you good luck in trading to you all!
——————
✈️ CONTACT TO JOIN GOLD SIGNALS VIP👉🏻 @goldvip_contact

😍 OR JOIN VIP IN BOT👉🏻@GoldSignalsVipPaymentBot""",
    """📊EURUSD: Local Correction Ahead! Buy!

🆓SIGNAL DETAILS 
——————
ENTER: Long trade 
CURRENT PRICE:  1.08132
STOP LOSS:    1.08036
TAKE PROFIT: 1.08275
——————
🔔SUGGESTED RISK:
1% of the account for each trade

👑Wish you good luck in trading to you all!
——————
📣VIP PRIVILEGES:

🔖Safe strategy 
🔖Small account friendly 
🔖Easy signup 

✈️ TEXT TO JOIN VIP👉🏻 @goldvip_contact

😍 OR JOIN VIP IN BOT👉🏻@GoldSignalsVipPaymentBot""",
    """📊BTCUSD: Market Is Looking Up! Buy!

🆓SIGNAL DETAILS 
——————
ENTER: Long trade 
CURRENT PRICE:  84,994.20
STOP LOSS:   84,755.28
TAKE PROFIT: 85,351.46
——————
🔔SUGGESTED RISK:
1% of the account for each trade

👑Wish you good luck in trading to you all!
——————
✈️ CONTACT TO JOIN GOLD SIGNALS VIP👉🏻 @goldvip_contact

😍 OR JOIN VIP IN BOT👉🏻@GoldSignalsVipPaymentBot"""
]

for msg in messages:
    print(extract_gold_signals(msg))
    print(is_new_postion_gold_signals(msg))