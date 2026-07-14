from features import preprocess
from predict import result
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded, 
    _rate_limit_exceeded_handler, # type: ignore[arg-type]
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/predict')
@limiter.limit("5/minute")
async def predict(request: Request, data: dict) -> dict:
    # Prediction (home_win: 0 or 1)
    data = preprocess(data)
    res = result(data)
    return res