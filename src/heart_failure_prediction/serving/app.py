from contextlib import asynccontextmanager
import logging
import os.path

from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd
from sklearn.pipeline import Pipeline

from heart_failure_prediction.config import MODEL_DIR
from heart_failure_prediction.serving.schemas import HeartDiseaseRecord

logger = logging.getLogger(__name__)

models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    model_folder = MODEL_DIR
    model_name = 'model.joblib'
    model_path = os.path.join(model_folder, model_name)
    try:
        model = joblib.load(model_path)
        models['model'] = model
        logger.info('Model loaded successfully')
    except FileNotFoundError:
        logger.error(f"Couldn't read model from path {model_path}")

    yield

    models.clear()


app = FastAPI(lifespan=lifespan)


@app.get('/health')
async def health():
    model = models.get('model')

    if model is None:
        raise HTTPException(status_code=503, detail='Service unavailable')

    return {'status': 'working'}


@app.post('/predict')
async def predict(record: HeartDiseaseRecord):
    model: Pipeline = models.get('model')

    if model is None:
        logger.error("Model wasn't loaded")
        raise HTTPException(status_code=503, detail='Service unavailable')

    try:
        data = pd.DataFrame.from_records([record.model_dump()])
        pred = model.predict(data)
        pred_proba = model.predict_proba(data)

        return {
            'HeartDisease': int(pred[0]),
            'Probability-positive': float(pred_proba[0][1]),
            'Probability-negative': float(pred_proba[0][0]),
        }

    except Exception as e:
        logger.error(f'Error during prediction phase: {e}')
        raise HTTPException(status_code=500) from e
