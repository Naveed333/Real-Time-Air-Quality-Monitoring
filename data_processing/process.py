import pandas as pd


def process_data(df):
    # Clean the data by dropping rows with missing values (if any)
    df = df.dropna()

    # Additional data processing can be done here
    # For example: Add new columns, scale values, etc.

    return df
