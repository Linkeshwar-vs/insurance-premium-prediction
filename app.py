from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.user_input import UserInput
from model.predict import predict_output, model, MODEL_VERSION
from schema.prediction_response import PredictionResponse
from database import engine, SessionLocal
from models import Base, Prediction


import os

SERVER_ID = os.getenv("SERVER_ID", "unknown")


app=FastAPI()

Base.metadata.create_all(bind=engine)

@app.get('/')
def home():
    return {
        'message': 'Insurance Premium Prediction API',
        'server': SERVER_ID
    }

#Health check endpoint

@app.get("/health")
def health():
    return {
        "status": "OK",
        "version": MODEL_VERSION,
        "model_loaded":model is not None
    }

@app.post('/predict', response_model= PredictionResponse)
def predict_premium(user_data : UserInput):

    input_data = {
        "bmi": user_data.bmi,
        "age_group": user_data.age_group,
        "lifestyle_risk":user_data.lifestyle_risk,
        "city_tier": user_data.city_tier,
        "income_lpa": user_data.income_lpa,
        "occupation": user_data.occupation
    }

    try:
        result = predict_output(input_data)

        db = SessionLocal()

        prediction = Prediction(
            bmi=user_data.bmi,
            age_group=user_data.age_group,
            lifestyle_risk=user_data.lifestyle_risk,
            city_tier=user_data.city_tier,
            income_lpa=user_data.income_lpa,
            occupation=user_data.occupation,
            predicted_premium=result
        )

        db.add(prediction)
        db.commit()

        db.close()

        return JSONResponse(
            status_code=200,
            content={"Response :": result}
        )
    except Exception as e:
        return JSONResponse(status_code=500, content = str(e))
