# train_model.py

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import joblib

# Example data (replace with your real dataset)
data = {
    "pm10": [100, 120, 140, 160, 180],
    "co": [1.2, 1.5, 1.1, 2.2, 1.0],
    "temperature": [20, 21, 22, 23, 24],
    "humidity": [45, 50, 55, 60, 65],
    "pm25": [80, 90, 100, 110, 120],  # Target variable
}

df = pd.DataFrame(data)

# Split data into features (X) and target (y)
X = df[["pm10", "co", "temperature", "humidity"]]
y = df["pm25"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Save model to disk (pkl file)
joblib.dump(model, "machine_learning/air_quality_model.pkl")


# Define predict_air_quality function
def predict_air_quality(features, days=1):
    predictions = []
    for _ in range(days):
        prediction = model.predict([features])
        predictions.append(prediction[0])
        # Simple logic to update features for the next day (for example purposes)
        features = [
            features[0] + 10,
            features[1] + 0.1,
            features[2] + 1,
            features[3] + 1,
        ]  # Update features for next prediction
    return predictions
