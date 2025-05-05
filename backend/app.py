from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import os

app = Flask(__name__)

# Load models (assuming they are in ../models/)
MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'models')
models = {
    "logistic_regression": joblib.load(os.path.join(MODEL_DIR, 'logistic_regression.pkl')),
    "svm": joblib.load(os.path.join(MODEL_DIR, 'svm.pkl')),
    "decision_tree": joblib.load(os.path.join(MODEL_DIR, 'decision_tree.pkl')),
    "random_forest": joblib.load(os.path.join(MODEL_DIR, 'random_forest.pkl')),
}

@app.route("/")
def home():
    return render_template("../frontend/index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    features = np.array(data["features"]).reshape(1, -1)
    model_name = data.get("model", "logistic_regression")
    
    model = models.get(model_name)
    if not model:
        return jsonify({"error": "Model not found"}), 400

    prediction = model.predict(features)
    return jsonify({"prediction": int(prediction[0])})

if __name__ == "__main__":
    app.run(debug=True)
