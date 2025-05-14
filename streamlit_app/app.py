import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import logging
import joblib
# from data_ingestion.api_client import fetch_air_quality_data
from machine_learning.train_model import predict_air_quality  # Import predict function

from data_ingestion.api_client import fetch_air_quality_data

# Set up logging
logger = logging.getLogger(__name__)

# Load the trained model
model = joblib.load("machine_learning/air_quality_model.pkl")


# Country and city mapping
country_city_map = {
    "US": ["Raleigh", "New York"],
    "UK": ["London"],
    "Canada": ["Toronto", "Vancouver"],
}


# Function to predict the PM2.5 value for the next day using the model
def predict_next_day_pm25(features):
    prediction = model.predict([features])  # Predict PM2.5 for the next day
    return prediction[0]


def send_alert(aqi):
    if aqi > 100:  # Example threshold
        st.warning("Unhealthy Air Quality!")
    elif aqi > 50:
        st.info("Moderate Air Quality")
    else:
        st.success("Good Air Quality")


def display_dashboard(data):
    st.title("Real-Time Air Quality Monitoring")

    # Display City and Country information
    if "city" in data.columns:
        st.write("City:", data["city"].iloc[0])  # Use .iloc[0] for the first row
    else:
        st.write("City: Not Available")

    if "country" in data.columns:
        st.write("Country:", data["country"].iloc[0])
    else:
        st.write("Country: Not Available")

    # Display latitude and longitude
    if "latitude" in data.columns and "longitude" in data.columns:
        st.write(f"Latitude: {data['latitude'].iloc[0]}")
        st.write(f"Longitude: {data['longitude'].iloc[0]}")
    else:
        st.write("Location data (Latitude/Longitude): Not Available")

    # Display AQI data if available
    if "aqi" in data.columns:
        st.line_chart(data["aqi"])
    else:
        st.write("AQI data not available!")


def process_data(df):
    # Clean the data by dropping rows with missing values (if any)
    df = df.dropna()

    # Ensure the 'aqi' column exists and handle it correctly
    if "aqi" in df.columns:
        print("AQI column found.")
    else:
        print("AQI column not found!")

    return df


def display_map(lat, long):
    # Create a map centered around the selected lat/long
    map_location = folium.Map(location=[lat, long], zoom_start=12)
    folium.Marker([lat, long], popup="Air Quality Location").add_to(map_location)
    return st_folium(map_location, width=700, height=500)


def main():
    # api_key = "e19e6cb107mshaa406fe397a20abp162c3cjsn670651231384"
    # api_key = "89307e48a2msh4d3b023c0ca78abp19417fjsnf0868fff2816"
    api_key = "475e129254mshf6f9912ec6b5fb6p1b2ed5jsne0122d27e56a"

    # Allow the user to select a country
    selected_country = st.selectbox("Select Country", ["US", "UK", "Canada"])

    # Based on selected country, allow the user to select a city
    selected_city = st.selectbox("Select City", country_city_map[selected_country])

    # Fetch air quality data from the API
    data = fetch_air_quality_data(api_key, selected_city, selected_country)

    if data:
        # Extract the 'data' key for the air quality records
        df = pd.DataFrame(data["data"])

        # Display the data for inspection
        st.write(df.head())  # Display the first few rows to inspect data

        # Check for required columns
        if "pm10" in df.columns and "co" in df.columns:
            # Fallback for missing columns
            temperature = (
                df["temperature"].mean() if "temperature" in df.columns else 20
            )  # Default value for missing temperature
            humidity = (
                df["humidity"].mean() if "humidity" in df.columns else 50
            )  # Default value for missing humidity

            features = [
                df["pm10"].mean(),
                df["co"].mean(),
                temperature,
                humidity,
            ]

            # Predict next day's PM2.5 using the model
            next_day_pm25 = predict_next_day_pm25(features)
            st.write(f"Predicted PM2.5 for the next day: {next_day_pm25:.2f} µg/m³")

            # Send an alert based on the AQI value
            if "aqi" in df.columns:
                send_alert(df["aqi"].iloc[0])
            else:
                st.write("AQI data not available!")

            # Display the processed data
            display_dashboard(df)

            # Display the map with air quality location
            if "latitude" in df.columns and "longitude" in df.columns:
                display_map(df["latitude"].iloc[0], df["longitude"].iloc[0])
            else:
                st.write("Latitude and Longitude data not available.")
        else:
            st.write("Missing required columns in the data!")


if __name__ == "__main__":
    main()
