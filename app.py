from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)


@app.route('/api/recommend_products', methods=['POST'])
def recommend_products():
    data = request.get_json()
    user_id = data['user_id']

    # AIサービスにリクエストを送信
    ai_response = requests.post('http://ai-domain:5005/recommend', json={'user_id': user_id})
    recommended_products = ai_response.json()

    return jsonify(recommended_products), 200


@app.route('/api/update_model', methods=['POST'])
def update_model():
    data = request.get_json()
    try:
        response = requests.post('http://ai-domain:5005/update_model', json=data)
        response_data = response.json()
        message = response_data.get('message', 'Update failed')
    except requests.exceptions.RequestException as e:
        message = f'Update failed: {str(e)}'
    
    return jsonify({'message': message})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5004)