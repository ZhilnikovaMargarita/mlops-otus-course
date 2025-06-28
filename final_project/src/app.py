import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from loguru import logger

import holidays
# from pandarallel import pandarallel

from src.inference import load_model, predict
from src.utils import additional_columns, get_city, get_time_feats, get_cnts

from prometheus_client import Counter

TRESHOLD = os.getenv("TRESHOLD", default=0.6)

CANCELLATIONS_COUNTER = Counter("cancelletions", "Number of taxi cancelletions")

# pandarallel.initialize(progress_bar=True, nb_workers=4)


logger.info("Loading pkl model")
# MODEL_PATH = os.path.join("models", "model.joblib")
MODEL_PATH = os.path.join("models", "model.pkl")
MODEL = load_model(MODEL_PATH)
logger.info("Model loaded")


app = FastAPI()

# class IrisFeatures(BaseModel):
#     """Iris features"""
#     # sepal_length: float
#     # sepal_width: float
#     # petal_length: float
#     # petal_width: float
#     SepalLengthCm: float
#     SepalWidthCm: float
#     PetalLengthCm: float
#     PetalWidthCm: float

@app.get("/")
def health_check() -> dict:
    """Health check"""
    return {"status": "ok"}


class TripFeatures(BaseModel):
    dist: str = "4611.506"
    due: str = "2014-03-30 11:30:00"
    lat: float = "55.77" # точка, куда делали заказ
    lon: float = "37.68" # точка, куда делали заказ
    f_class: str = None # дополнительные опции заказа в приложении такси
    s_class: str = None
    t_class: str = None


def prepare_clear_features(features: TripFeatures) -> pd.DataFrame:
    df = pd.DataFrame([features.model_dump()])
    hdays = holidays.CountryHoliday('RU')
    df['due'] = pd.to_datetime(df['due'])
    df = get_time_feats(df.rename(columns={'due': 'datetime'}), hdays)
    df = get_city(df)
    df['coord'] = df['lon'].astype(str) + '_' + df['lat'].astype(str)
    df['datetime'] = df['datetime'].round('min')
    print("df:")
    print(df)

    coord_cnts = df.groupby('coord')['dist'].count()
    print("coord_cnts:")
    print(coord_cnts)

    df['is_airport'] = df['location'].str.contains('airport').fillna(0).astype(int)
    df = pd.get_dummies(
        df, columns=[
                'f_class', 's_class', 
                't_class','city'
            ]
    )
    df = df.drop(columns=['location'])

    for col in additional_columns:
        if col not in df.columns:
            df[col] = None
    return df

@app.post("/predict")
def make_prediction(features: TripFeatures) -> dict:
    """Make a prediction by model"""
    try:
        logger.info("features:")
        logger.info(f"{features}")
        data = prepare_clear_features(features)
        prediction = predict(MODEL, data)
        logger.info("prediction:")
        logger.info(f"{prediction}")
        prob = float(prediction.data[0][0])
        verdict = prob > TRESHOLD
        if verdict:
            CANCELLATIONS_COUNTER.inc()
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(
            status_code=500, 
            detail="An error occurred during prediction"
        )
    
    return {"verdicts": verdict, "prediction": round(prob, 3), "treshold": treshold}
