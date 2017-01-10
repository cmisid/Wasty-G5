from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():
    payload = {
        'confiance': 0.8,
        'tag': 'meuble'
    }
    return jsonify(payload)


@app.route('/optimize-itinerary', methods=['POST'])
def optimize_itinerary():
    payload = request.get_json()
    start = payload['start']
    points = payload['points']



    return jsonify(points)


if __name__ == '__main__':
    app.run(debug=True)
