from features import preprocess
from predict import result
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


class PredictionInput(BaseModel):
    away_team: str = Field(..., min_length=1)
    home_team: str = Field(..., min_length=1)
    away_elo_pre: float = Field(..., ge=0)
    home_elo_pre: float = Field(..., ge=0)
    elo_prob_away: float = Field(..., ge=0, le=1)
    elo_prob_home: float = Field(..., ge=0, le=1)


limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title='Crossroads Baseball Predictor', version='1.0.0')
app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,  # type: ignore[arg-type]
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/health')
async def health() -> dict:
    return {'status': 'ok'}


@app.post('/predict')
@limiter.limit('5/minute')
async def predict(request: Request, payload: PredictionInput) -> dict:
    payload_dict = payload.model_dump()
    processed = preprocess(payload_dict)
    prediction = result(processed)
    return prediction