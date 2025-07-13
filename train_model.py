
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

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
encoder = LabelEncoder()
df["outcome"] = encoder.fit_transform(df["outcome"])  # 'Low' -> 0, 'Medium' -> 1, 'High' -> 2

# Separate features (X) and target variable (y)
X = df.drop(columns=["outcome"])
y = df["outcome"]

# Normalize numerical data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Train the Model (Random Forest)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the Model
y_pred = model.predict(X_test)
print("Model Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Save the model, scaler, and encoder for later use
joblib.dump(model, 'infant_health_model.pkl')
joblib.dump(scaler, 'scaler.pkl')
joblib.dump(encoder, 'encoder.pkl')
