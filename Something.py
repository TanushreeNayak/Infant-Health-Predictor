import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from flask import Flask, request, jsonify
import Pyhealth

# Creating Infant Health Data
data = {
    "age_months": np.random.randint(6, 13, 50),  # Age in months (6-12 months)
    "weight_kg": np.random.uniform(5.5, 10, 50),  # Infant weight (kg)
    "height_cm": np.random.uniform(60, 80, 50),  # Infant height (cm)
    "heart_rate": np.random.randint(90, 160, 50),  # Normal range for infants
    "oxygen_level": np.random.uniform(85, 100, 50),  # Blood oxygen level (SpO2)
    "temperature": np.random.uniform(36, 39, 50),  # Body temperature (°C)
    "feeding_frequency": np.random.randint(5, 12, 50),  # Feeds per day
    "sleep_hours": np.random.uniform(10, 15, 50),  # Average sleep per day
    "outcome": np.random.choice(["Low", "Medium", "High"], 50)  # Risk Level
}

df = pd.DataFrame(data)

# Preprocessing Data
# Convert categorical target variable to numerical
encoder = LabelEncoder()
df["outcome"] = encoder.fit_transform(df["outcome"])  # 'Low' -> 0, 'Medium' -> 1, 'High' -> 2

# Separate features (X) and target variable (y)
X = df.drop(columns=["outcome"])
y = df["outcome"]

# Normalize numerical data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 3️⃣ Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# 4️⃣ Train the Model (Random Forest)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5️⃣ Evaluate the Model
y_pred = model.predict(X_test)
print("Model Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

from flask import Flask, request, jsonify

# app = Flask(__name__)

# @app.route('/predict', methods=['POST'])
# def predict():
#     input_data = request.get_json()
#     input_df = pd.DataFrame([input_data])
#     input_scaled = scaler.transform(input_df)
#     prediction = model.predict(input_scaled)
#     predicted_label = encoder.inverse_transform(prediction)[0]
#     return jsonify({'predicted_risk': predicted_label})

# if __name__ == '__main__':
#     app.run(debug=True)
    

# import requests

# url = "http://127.0.0.1:5000/predict"
# data = {
#     "age_months": 9,
#     "weight_kg": 8.5,
#     "height_cm": 73,
#     "heart_rate": 130,
#     "oxygen_level": 96,
#     "temperature": 37.2,
#     "feeding_frequency": 8,
#     "sleep_hours": 13.5
# }

# response = requests.post(url, json=data)
# print(response.json())

# 6️⃣ API for Predictions (Flask Deployment)

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    # Validate incoming data to ensure all expected keys are present
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
        input_scaled = scaler.transform([input_data])
        prediction = model.predict(input_scaled)[0]
        predicted_label = encoder.inverse_transform([prediction])[0]
        return jsonify({"Predicted Outcome": predicted_label})
    except ValueError as e:
        return jsonify({"error": f"Invalid input data: {e}"}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)