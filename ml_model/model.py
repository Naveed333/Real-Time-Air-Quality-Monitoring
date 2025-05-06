from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib
import logging
from logging import getLogger

logger = getLogger(__name__)


# Prepare data for machine learning
def prepare_ml_data(df):
    X = df[["hour", "pm25", "pm10"]]  # Example features
    y = df["aqi"]
    return train_test_split(X, y, test_size=0.2)


# Train the regression model
def train_model(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)
    logger.info("Model successfully trained")
    return model


# Save model to disk
def save_model(model, filename):
    try:
        joblib.dump(model, filename)
        logger.info(f"Model saved to {filename}")
    except Exception as e:
        logger.error(f"Error saving model: {e}")
