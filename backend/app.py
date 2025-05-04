from flask import Flask, request, jsonify, send_from_directory
import pickle
import numpy as np
import os
import pkgutil
import sys
from importlib.abc import MetaPathFinder
import importlib.resources as pkg_resources
from flask_cors import CORS  # Add this import

app = Flask(__name__, static_folder='../frontend')
CORS(app) 

if not hasattr(pkgutil, 'ImpImporter'):
    # Monkey-patch for Python 3.12+ compatibility
    pkgutil.ImpImporter = type('FakeImpImporter', (MetaPathFinder,), {})
    sys.meta_path.append(pkgutil.ImpImporter())


# Load model
model = pickle.load(open('models/random_forest.pkl', 'rb'))

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if len(data['features']) != 30:
            return jsonify({'error': 'Exactly 30 features required'}), 400
            
        features = np.array(data['features']).reshape(1, -1)
        prediction = model.predict(features)
        return jsonify({
            'prediction': int(prediction[0]),
            'confidence': float(np.max(model.predict_proba(features)))
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def serve_frontend():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../frontend', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
    