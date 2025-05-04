// Breast cancer feature names (30 total)
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

const API_URL = 'https://your-backend.onrender.com/predict';

// Generate input fields
const container = document.getElementById('input-container');
featureNames.forEach(feature => {
    const group = document.createElement('div');
    group.className = 'input-group';
    group.innerHTML = `
        <label for="${feature}">${feature.replace(/_/g, ' ')}:</label>
        <input type="number" step="0.0001" id="${feature}" required>
    `;
    container.appendChild(group);
});

// Prediction handler
document.getElementById('predict-btn').addEventListener('click', async () => {
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = '<p>Processing...</p>';
    
    try {
        const features = featureNames.map(f => {
            const val = parseFloat(document.getElementById(f).value);
            if (isNaN(val)) throw new Error(`Invalid value for ${f}`);
            return val;
        });

        const response = await fetch('https://your-render-backend-url.onrender.com/predict',{
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ features })
        });

        const data = await response.json();
        
        if (response.ok) {
            const predictionText = data.prediction === 1 ? 
                'Benign (non-cancerous)' : 'Malignant (cancerous)';
            const confidence = (data.confidence * 100).toFixed(2);
            
            resultDiv.className = data.prediction === 1 ? 'benign' : 'malignant';
            resultDiv.innerHTML = `
                <h2>Prediction: ${predictionText}</h2>
                <p>Confidence: ${confidence}%</p>
            `;
        } else {
            throw new Error(data.error || 'Prediction failed');
        }
    } catch (error) {
        resultDiv.className = 'error';
        resultDiv.innerHTML = `<p>Error: ${error.message}</p>`;
        console.error('Prediction error:', error);
    }
});

