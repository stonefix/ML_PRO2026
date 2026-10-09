import time
import uuid
from contextlib import asynccontextmanager

import joblib
import pandas as pd
from fastapi import BackgroundTasks, FastAPI, HTTPException
from pydantic import BaseModel, Field

from churn import db
from churn.config import settings


class Features(BaseModel):
    model_config = {"extra": "forbid"}

    attack: int = Field(ge=1, le=255)
    defense: int = Field(ge=1, le=255)
    hp: int = Field(ge=1, le=255)
    sp_attack: int = Field(ge=1, le=255)
    sp_defense: int = Field(ge=1, le=255)
    speed: int = Field(ge=1, le=255)
    height_m: float = Field(gt=0, le=20.0)
    weight_kg: float = Field(gt=0, le=1000.0)
    percentage_male: float | None = Field(default=None, ge=0, le=100)
    generation: int = Field(ge=1, le=9, description="Generation Pokémon")
    type: str


class Prediction(BaseModel):
    #model_config = {"protected_namespaces": ()}

    score: float
    is_legendary: bool
    model_version: str
    request_id: str
    latency_ms: float


@asynccontextmanager
async def lifespan(app: FastAPI):
    bundle = joblib.load(settings.model_path)
    app.state.pipeline = bundle["pipeline"]
    app.state.meta = bundle["metadata"]
    app.state.version = bundle["metadata"]["model_version"]

    db.init()
    yield
    app.state.pipeline = None


app = FastAPI(title="churn-service", version="1.0", lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "ok", "model_version": getattr(app.state, "version", "unknown")}

@app.get("/ready")
def ready():
    if getattr(app.state, "pipeline", "None") is  None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {"status": "ready"}



@app.post("/v1/predict")
def predict(x: Features, bg: BackgroundTasks) -> Prediction:
    t0 = time.perf_counter()
    request_id = str(uuid.uuid4())
    payload = x.model_dump()  # x.dict() in pydantic v1
    frame = pd.DataFrame([payload]).reindex(columns=app.state.meta["features"])

    score = float(app.state.pipeline.predict_proba(frame)[0, 1])

    latency_ms = round((time.perf_counter() - t0) * 1000, 2)

    bg.add_task(db.save_prediction, request_id, payload, score, app.state.version, latency_ms)

    is_legendary = score >= app.state.meta["threshold"]

    return Prediction(score=score, is_legendary=is_legendary, model_version = app.state.version, request_id=request_id, latency_ms=latency_ms)








