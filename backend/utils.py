import numpy as np
from sklearn.preprocessing import StandardScaler

def preprocess_input(features):
    """Standardize input features using training data scaler"""
    scaler = StandardScaler()
    # In practice, fit scaler on training data and save/load it
    return scaler.fit_transform(np.array(features).reshape(1, -1))