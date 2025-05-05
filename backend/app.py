from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import joblib
import numpy as np
import os

# Set Flask to serve from the frontend folder
app = Flask(__name__, template_folder="../frontend", static_folder="../frontend")
CORS(app)  # Allow CORS for frontend-backend communication if needed

# Load models from the models directory
MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'models')
models = {
    "logistic_regression": joblib.load(os.path.join(MODEL_DIR, 'logistic_regression.pkl')),
    "svm": joblib.load(os.path.join(MODEL_DIR, 'svm.pkl')),
    "decision_tree": joblib.load(os.path.join(MODEL_DIR, 'decision_tree.pkl')),
    "random_forest": joblib.load(os.path.join(MODEL_DIR, 'random_forest.pkl')),
}

# Serve index.html from the frontend folder
@app.route("/")
def home():
    return render_template("index.html")

# Handle prediction
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        if not data or "features" not in data:
            return jsonify({"error": "Missing 'features' in request"}), 400

        features = np.array(data["features"]).reshape(1, -1)
        model_name = data.get("model", "logistic_regression")

        model = models.get(model_name)
        if not model:
            return jsonify({"error": "Model not found"}), 400

        prediction = model.predict(features)

        # Try to get confidence score (if model supports predict_proba)
        if hasattr(model, "predict_proba"):
            confidence = float(np.max(model.predict_proba(features)))
        else:
            confidence = 1.0  # fallback when confidence can't be calculated

        return jsonify({
            "prediction": int(prediction[0]),
            "confidence": confidence
        })

    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({"error": str(e)}), 500

# Serve static files (styles.css, script.js, etc.)
@app.route('/<path:filename>')
def serve_static_files(filename):
    return send_from_directory('../frontend', filename)

if __name__ == "__main__":
    app.run(debug=True)
