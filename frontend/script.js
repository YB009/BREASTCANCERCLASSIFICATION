const API_URL = 'http://localhost:5000/predict'; // Change to your Render URL when deploying

const featureNames = [
    "radius_mean", "texture_mean", "perimeter_mean", "area_mean",
    "smoothness_mean", "compactness_mean", "concavity_mean",
    "concave_points_mean", "symmetry_mean", "fractal_dimension_mean",
    "radius_se", "texture_se", "perimeter_se", "area_se",
    "smoothness_se", "compactness_se", "concavity_se",
    "concave_points_se", "symmetry_se", "fractal_dimension_se",
    "radius_worst", "texture_worst", "perimeter_worst", "area_worst",
    "smoothness_worst", "compactness_worst", "concavity_worst",
    "concave_points_worst", "symmetry_worst", "fractal_dimension_worst"
];

document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('input-container');
    featureNames.forEach(feature => {
        const div = document.createElement('div');
        div.className = 'input-group';
        div.innerHTML = `
            <label for="${feature}">${feature.replace(/_/g, ' ')}:</label>
            <input type="number" step="0.0001" id="${feature}" required>
        `;
        container.appendChild(div);
    });
});

document.getElementById('predict-btn').addEventListener('click', async () => {
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = '<p>Processing...</p>';
    resultDiv.className = '';
    
    try {
        const features = featureNames.map(f => {
            const val = parseFloat(document.getElementById(f).value);
            if (isNaN(val)) throw new Error(`Invalid value for ${f}`);
            return val;
        });

        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ features })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        const predictionText = data.prediction === 1 ? 
            'Benign (non-cancerous)' : 'Malignant (cancerous)';
        const confidence = (data.confidence * 100).toFixed(2);
        
        resultDiv.className = data.prediction === 1 ? 'benign' : 'malignant';
        resultDiv.innerHTML = `
            <h2>Prediction: ${predictionText}</h2>
            <p>Confidence: ${confidence}%</p>
        `;
    } catch (error) {
        resultDiv.className = 'error';
        resultDiv.innerHTML = `<p>Error: ${error.message}</p>`;
        console.error('Prediction error:', error);
    }
});