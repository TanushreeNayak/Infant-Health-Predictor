
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import joblib

# Load the model, scaler, and encoder
model = joblib.load('infant_health_model.pkl')
scaler = joblib.load('scaler.pkl')
encoder = joblib.load('encoder.pkl')

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    # Validate incoming data
    expected_keys = [
        "age_months", "weight_kg", "height_cm", "heart_rate",
        "oxygen_level", "temperature", "feeding_frequency", "sleep_hours"
    ]
    if not all(key in data for key in expected_keys):
        return jsonify({"error": "Missing one or more required input parameters"}), 400

    try:
        input_data = np.array([
            data["age_months"], data["weight_kg"], data["height_cm"],
            data["heart_rate"], data["oxygen_level"], data["temperature"],
            data["feeding_frequency"], data["sleep_hours"]
        ])
        input_scaled = scaler.transform([input_data])  # Scale the input data
        prediction = model.predict(input_scaled)[0]  # Get the prediction
        predicted_label = encoder.inverse_transform([prediction])[0]  # Decode the prediction

        return jsonify({"Predicted Outcome": predicted_label})

    except ValueError as e:
        print(f"Error during prediction: {e}")
        return jsonify({"error": f"Internal server error: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
