from features import elo_ratings
from predict import result
from fastapi import FastAPI
import pandas as pd

app = FastAPI()

@app.post('/predict')
async def predict(df: pd.DataFrame):
    # Prediction (home_win: 0 or 1)
    res = result(df)
    return res