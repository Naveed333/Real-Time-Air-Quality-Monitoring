import pandas as pd


def process_data(df):
    # Clean the data by dropping rows with missing values (if any)
    df = df.dropna(
        subset=["pm25", "pm10", "co", "temperature", "humidity", "city", "aqi"]
    )

    # Additional data processing can be done here
    # For example: Add new columns, scale values, etc.

    return df
