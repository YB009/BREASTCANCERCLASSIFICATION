from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np

app = Flask(__name__)

# Configure CORS for specific origins
CORS(app, resources={
    r"/predict": {
        "origins": [
            "https://your-frontend.onrender.com",  # Your frontend URL
            "http://localhost:*",                 # For local testing
            "https://your-backend.onrender.com"    # Your backend URL
        ],
        "methods": ["POST"],
        "allow_headers": ["Content-Type"]
    }
})

# Load model
model = pickle.load(open('models/random_forest.pkl', 'rb'))

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        features = np.array(data['features']).reshape(1, -1)
        prediction = model.predict(features)
        return jsonify({
            'prediction': int(prediction[0]),
            'confidence': float(np.max(model.predict_proba(features)))
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/')
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)