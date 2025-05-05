from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import numpy as np
import os

# Initialize Flask app with proper paths
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, '..', 'models', 'random_forest.pkl')
FRONTEND_DIR = os.path.join(BASE_DIR, '..', 'frontend')

# Load the correct model
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Failed to load model: {str(e)}")

# Serve static files
@app.route('/')
def serve_frontend():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(FRONTEND_DIR, path)

# Prediction endpoint
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        
        if not data or "features" not in data:
            return jsonify({"error": "Missing 'features' in request"}), 400
            
        features = np.array(data["features"])
        
        # Validate input features
        if len(features) != 30:
            return jsonify({
                "error": f"Expected 30 features, got {len(features)}",
                "required_features": [
                    "radius_mean", "texture_mean", "perimeter_mean", 
                    # ... list all 30 feature names ...
                ]
            }), 400

        # Reshape and predict
        features = features.reshape(1, -1)
        prediction = model.predict(features)
        
        # Get confidence score
        if hasattr(model, "predict_proba"):
            confidence = float(np.max(model.predict_proba(features)))
        else:
            confidence = 1.0

        return jsonify({
            "prediction": int(prediction[0]),
            "confidence": confidence,
            "model_used": "random_forest"
        })

    except Exception as e:
        app.logger.error(f"Prediction error: {str(e)}")
        return jsonify({
            "error": "Prediction failed",
            "details": str(e)
        }), 500

# Health check endpoint
@app.route("/health")
def health_check():
    return jsonify({
        "status": "healthy",
        "model_loaded": True,
        "expected_features": 30
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)