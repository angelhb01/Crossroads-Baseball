import joblib
import os

# Load Logistic Regression model
model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'Logistic_Regression_model.pkl')
model = joblib.load(model_path)
features = ['away_encode', 'home_encode', 'away_elo_pre', 'home_elo_pre', 'elo_prob_away', 'elo_prob_home']

def result(data: dict) -> dict:
    X = data[features]
    res = model.predict(X)
    return res