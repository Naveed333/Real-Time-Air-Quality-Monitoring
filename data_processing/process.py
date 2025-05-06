import pandas as pd


# Data transformation function: Handle missing values, feature engineering, etc.
def process_data(df):
    try:
        df = df.dropna()  # Remove missing data
        df["hour"] = df["timestamp"].dt.hour  # Extract the hour of the day as a feature
        return df
    except Exception as e:
        print(f"Error processing data: {e}")
        return None
