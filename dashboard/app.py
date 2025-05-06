import streamlit as st

# from data_ingestion.ingest import fetch_air_quality_data
# from data_processing.process import process_data
# from ml_model.model import prepare_ml_data, train_model, save_model
# import logging
import pandas as pd

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Now your imports should work
from data_ingestion.ingest import fetch_air_quality_data
from data_processing.process import process_data
from ml_model.model import prepare_ml_data, train_model, save_model


# Streamlit app for visualization and alerts
def send_alert(aqi):
    if aqi > 100:  # Example threshold
        st.warning("Unhealthy Air Quality!")
    elif aqi > 50:
        st.info("Moderate Air Quality")
    else:
        st.success("Good Air Quality")


def display_dashboard(data):
    st.title("Real-Time Air Quality Monitoring")

    # Check if 'city_name' exists, and display it
    if "city_name" in data.columns:
        st.write("City:", data["city_name"].iloc[0])  # Use .iloc[0] for the first row
    else:
        st.write("City: Not Available")

    # Check if 'country_code' exists, and display it
    if "country_code" in data.columns:
        st.write("Country:", data["country_code"].iloc[0])
    else:
        st.write("Country: Not Available")

    # Display timestamp if available
    if "timestamp_utc" in data.columns:
        st.write("Timestamp (UTC):", data["timestamp_utc"].iloc[0])
    elif "timestamp_local" in data.columns:
        st.write("Timestamp (Local):", data["timestamp_local"].iloc[0])
    else:
        st.write("Timestamp: Not Available")

    # Display AQI data if available
    if "aqi" in data.columns:
        st.line_chart(data["aqi"])
    else:
        st.write("AQI data not available!")


import pandas as pd


def process_data(df):
    # Print the first few rows to check the structure
    print("First few rows of the data:", df.head())

    # Print the columns to inspect the DataFrame
    print("Columns in the DataFrame:", df.columns)

    # Clean the data by dropping rows with missing values (if any)
    df = df.dropna()

    # Ensure the 'aqi' column exists and handle it correctly
    if "aqi" in df.columns:
        print("AQI column found.")
    else:
        print("AQI column not found!")

    # You can add more feature engineering or transformations here if necessary
    return df


def main():
    api_key = "e19e6cb107mshaa406fe397a20abp162c3cjsn670651231384"
    latitude = "35.779"  # Example: London latitude
    longitude = "-78.638"  # Example: London longitude

    # Fetch air quality data from the API
    data = fetch_air_quality_data(api_key, latitude, longitude)

    if data:
        # Extract the 'data' key for the air quality records
        df = pd.DataFrame(data['data'])

        # Add metadata (city_name and country_code) to the DataFrame
        df['city_name'] = data['city_name']
        df['country_code'] = data['country_code']

        # Print the columns to verify
        print("Columns in the processed DataFrame:", df.columns)

        # Process the data (e.g., clean missing values, perform feature engineering)
        processed_data = process_data(df)

        # Display the processed data in the Streamlit dashboard
        display_dashboard(processed_data)

        # Send an alert based on the AQI value
        if 'aqi' in processed_data.columns:
            send_alert(processed_data["aqi"].iloc[0])
        else:
            print("AQI data not available!")

if __name__ == "__main__":
    main()
