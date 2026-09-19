import joblib
import os

import pandas as pd

# Load Logistic Regression model
model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'Logistic_Regression_model.pkl')
model = joblib.load(model_path)
features = ['away_encode', 'home_encode', 'away_elo_pre', 'home_elo_pre', 'elo_prob_away', 'elo_prob_home']


def result(data: dict) -> dict:
    row = {key: data.get(key) for key in features}
    X = pd.DataFrame([row], columns=features)
    res = model.predict(X)
    prediction = int(res[0])
    return {'prediction': prediction}