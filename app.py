from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/hello', methods=['POST'])
def handle_motion_detection():
    data = request.get_json()
    motion_detected = data.get('motion_detected')
    timestamp = data.get('timestamp')
    print(f'Motion detected: {motion_detected} at {timestamp}')

    return jsonify({'message': 'Data received successfully!'}), 200

if __name__ == '__main__':
    app.run()