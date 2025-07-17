import numpy as np
import joblib
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Load the model, scaler, and encoder
model = joblib.load('infant_health_model.pkl')
scaler = joblib.load('scaler.pkl')
encoder = joblib.load('encoder.pkl')

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:4173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictRequest(BaseModel):
    age_months: float
    weight_kg: float
    height_cm: float
    heart_rate: float
    oxygen_level: float
    temperature: float
    feeding_frequency: float
    sleep_hours: float

@app.post("/predicts")
def predict(request: PredictRequest):
    try:
        input_data = np.array([
            request.age_months, request.weight_kg, request.height_cm,
            request.heart_rate, request.oxygen_level, request.temperature,
            request.feeding_frequency, request.sleep_hours
        ])
        input_scaled = scaler.transform([input_data])  # Scale the input data
        prediction = model.predict(input_scaled)[0]  # Get the prediction
        predicted_label = encoder.inverse_transform([prediction])[0]  # Decode the prediction

        return {"Predicted Outcome": predicted_label}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

# To run: uvicorn app:app --reload