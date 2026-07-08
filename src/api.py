from features import elo_ratings
from predict import result
from fastapi import FastAPI, File
import pandas as pd

app = FastAPI()

@app.post('/predict')
def predict(file):
    # Create the elo rating features
    df = elo_ratings(file)

    # Prediction (home_win: 0 or 1)
    res = result(df)
    return res