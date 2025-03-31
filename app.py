from flask import Flask, request, jsonify
from extract_free_signal_pro import extract_free_signal_pro
from extract_anabel_signals import extract_anabel_signals

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
        msg = """SPY Set To Grow! BUY!

👩‍💻My dear friends,
SPY looks like it will make a good move, and here are the details:
The market is trading on 555.80 pivot level.
Bias - Bullish
———————
Goal - 569.99
Recommended Stop Loss - 549.79
————————
💐#SPY 
💹Time Frame : 12H (signal)
———————————
WISH YOU ALL LUCK🍀


"""

        # Call the function and get the result
        result = extract_anabel_signals(msg)

        # Return the result as JSON
        return jsonify({"success": True, "data": result}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)