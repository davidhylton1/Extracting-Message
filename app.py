from flask import Flask, request, jsonify
from extract_free_signal_pro import extract_free_signal_pro
from extract_anabel_signals import extract_anabel_signals
from extract_gold_signals import extract_gold_signals
from extract_top_trading_signals import extract_top_trading_signals
from extract_forex_gdp_signals import extract_forex_gdp_signals
from extract_fx_signals import extract_fx_signals
from extract_signal_provider import extract_signal_provider

import re
app = Flask(__name__)

@app.route('/extract_free_signal_pro', methods=['POST'])
def free_signal_pro():
    try:
        # Get the message from the request
        data = request.get_json()
        msg = data.get('message', '')

        # Call the function and get the result
        result = extract_free_signal_pro(msg)

        # Return the result as JSON
        return jsonify({"success": True, "data": result}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/extract_anabel_signals', methods=['GET'])
def anabel_signals():
    try:
        # Get the message from the request
        msg = """GBPUSD Expected Growth! BUY!

👩‍💻My dear followers,
I analysed this chart on GBPUSD and concluded the following:
The market is trading on 1.2904 pivot level.
Bias - Bullish

Target - 1.2929
————————
💐#GBPUSD 
💹Time Frame :  1H (forecast)
———————————
WISH YOU ALL LUCK🍀


"""

        # Call the function and get the result
        result = extract_anabel_signals(msg)

        # Return the result as JSON
        return jsonify({"success": True, "data": result}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/extract_gold_signals', methods=['GET'])
def gold_signals():
    try:
        # Get the message from the request
        msg = """📊GOLD: Will Go Up! Buy!

🆓SIGNAL DETAILS 
——————
ENTER: Long trade 
CURRENT PRICE:  3,071.33
STOP LOSS:    3,063.41
TAKE PROFIT: 3,083.22
——————
🔔SUGGESTED RISK:
1% of the account for each trade

👑Wish you good luck in trading to you all!
——————
✈️ CONTACT TO JOIN GOLD SIGNALS VIP👉🏻 @goldvip_contact

😍 OR JOIN VIP IN BOT👉🏻@GoldSignalsVipPaymentBot
"""

        # Call the function and get the result
        result = extract_gold_signals(msg)

        # Return the result as JSON
        return jsonify({"success": True, "data": result}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/extract_top_trading_signals', methods=['GET'])
def top_trading_signals():
    try:
        # Get the message from the request
        msg = """📈GBP-NZD Free Signal!

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
@toptradingsignalsfx
"""
        msg = re.sub(r"\bENTER\b", "", msg, flags=re.IGNORECASE)

        # Call the function and get the result
        result = extract_top_trading_signals(msg)

        # Return the result as JSON
        return jsonify({"success": True, "data": result}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/extract_forex_gdp_signals', methods=['GET'])
def forex_gdp_signals():
    try:
        # Get the message from the request
        msg = """🔽Forex Signal

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

New to Signals? Read the rules here: https://www.forexgdp.com/follow/
"""
        msg = re.sub(r"\bENTER\b", "", msg, flags=re.IGNORECASE)

        # Call the function and get the result
        result = extract_forex_gdp_signals(msg)

        # Return the result as JSON
        return jsonify({"success": True, "data": result}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
@app.route('/extract_fx_signals', methods=['GET'])
def fx_signals():
    try:
        # Get the message from the request
        msg = """#NZDJPY: Long Trade Explained🔼

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
https://www.tradingview.com/chart/NZDJPY/gbXLTrPq-NZDJPY-Long-Trade-Explained/
"""
        msg = re.sub(r"\bENTER\b", "", msg, flags=re.IGNORECASE)

        # Call the function and get the result
        result = extract_fx_signals(msg)

        # Return the result as JSON
        return jsonify({"success": True, "data": result}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
@app.route('/extract_signal_provider', methods=['GET'])
def signal_provider():
    try:
        # Get the message from the request
        msg = """🔅USOIL Is Bullish! Long!📈
- - - - - - - - 
Please, check our technical outlook for 📊USOIL.

The market is approaching a key horizontal level 71.913.

Considering the today's price action, probabilities will be high to see a movement to 73.911.
- - - - - - - - 
#freesignal #usoil
- - - - - - - -
🌐About VIP: signalprovider.org
❓FAQ: signalprovider.org/faq
📲: @signalprovidercontact
"""
        msg = re.sub(r"\bENTER\b", "", msg, flags=re.IGNORECASE)

        # Call the function and get the result
        result = extract_signal_provider(msg)

        # Return the result as JSON
        return jsonify({"success": True, "data": result}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500    
    
if __name__ == '__main__':
    app.run(debug=True)