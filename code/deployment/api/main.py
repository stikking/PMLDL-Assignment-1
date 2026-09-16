import joblib
import pandas as pd
from typing import Literal
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()
pipeline = joblib.load("models/titanic_pipeline.joblib")


class Passenger(BaseModel):
    pclass: int
    sex: Literal["male", "female"]
    age: float
    sibsp: int
    parch: int
    fare: float
    embarked: Literal["C", "Q", "S"]


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict")
def predict(passenger: Passenger):
    features = {
        "pclass": [passenger.pclass],
        "age": [passenger.age],
        "sibsp": [passenger.sibsp],
        "parch": [passenger.parch],
        "fare": [passenger.fare],
        "sex_male": [1 if passenger.sex == "male" else 0],
        "embarked_Q": [1 if passenger.embarked == "Q" else 0],
        "embarked_S": [1 if passenger.embarked == "S" else 0],
    }
    df = pd.DataFrame(features)
    df = df[pipeline.feature_names_in_]
    result = pipeline.predict(df)[0]
    return {"prediction": int(result)}
