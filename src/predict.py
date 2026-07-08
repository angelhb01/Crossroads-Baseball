import pandas as pd
import joblib

# Load Logistic Regression model
model = joblib.load('../models/Logistic_Regression_model.pkl')
features = ['year', 'month', 'day', 'away_elo_pre', 'home_elo_pre', 'elo_prob_away', 'elo_prob_home']

def result(df):
    X = df[features]
    res = model.predict(X)
    return res