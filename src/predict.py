import joblib
import os

# Load Logistic Regression model
model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'Logistic_Regression_model.pkl')
model = joblib.load(model_path)
features = ['year', 'month', 'day', 'away_elo_pre', 'home_elo_pre', 'elo_prob_away', 'elo_prob_home']

def result(df):
    X = df[features]
    res = model.predict(X)
    return res