import joblib
import pandas as pd


def run_prediction():
    model = joblib.load("ml_model/model.pkl")
    new_data = pd.read_csv("data/realtime/latest_aqi.csv")
    X_new = new_data[["pm25", "pm10", "co", "no2", "temperature"]]
    predictions = model.predict(X_new)
    new_data["predicted_aqi"] = predictions
    new_data.to_csv("data/predictions/today.csv", index=False)
