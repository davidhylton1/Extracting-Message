from flask import Flask, request, jsonify
from extract_free_signal_pro import extract_free_signal_pro

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

if __name__ == '__main__':
    app.run(debug=True)