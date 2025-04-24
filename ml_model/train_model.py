import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import joblib

df = pd.read_csv("data/processed/aqi.csv")
X = df[["pm25", "pm10", "co", "no2", "temperature"]]
y = df["aqi"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = LinearRegression()
model.fit(X_train, y_train)

joblib.dump(model, "ml_model/model.pkl")
