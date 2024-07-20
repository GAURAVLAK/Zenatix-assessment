import json
from flask import Flask, jsonify

app = Flask(__name__)

def get_latest_reading():
    try:
        with open('timestamp.txt', 'r') as file:
            lines = file.readlines()
            if lines:
                return json.loads(lines[-1])
    except FileNotFoundError:
        return None

@app.route('/latest', methods=['GET'])
def latest_reading():
    latest = get_latest_reading()
    if latest:
        return jsonify(latest)
    else:
        return jsonify({'error': 'No data found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

