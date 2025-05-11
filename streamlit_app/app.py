import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import logging
import joblib
from data_ingestion.api_client import fetch_air_quality_data
from machine_learning.train_model import predict_air_quality  # Import predict function

# Set up logging
logger = logging.getLogger(__name__)

# Load the trained model
model = joblib.load("machine_learning/air_quality_model.pkl")


# Function to predict the PM2.5 value for the next day using the model
def predict_next_day_pm25(features):
    prediction = model.predict([features])  # Predict PM2.5 for the next day
    return prediction[0]


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

    # Display City and Country information
    if "city_name" in data.columns:
        st.write("City:", data["city_name"].iloc[0])  # Use .iloc[0] for the first row
    else:
        st.write("City: Not Available")

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


def process_data(df):
    # Clean the data by dropping rows with missing values (if any)
    df = df.dropna()

    # Ensure the 'aqi' column exists and handle it correctly
    if "aqi" in df.columns:
        print("AQI column found.")
    else:
        print("AQI column not found!")

    return df


def main():
    api_key = "e19e6cb107mshaa406fe397a20abp162c3cjsn670651231384"  # Replace with your actual RapidAPI key
    # api_key = "89307e48a2msh4d3b023c0ca78abp19417fjsnf0868fff2816"  # Replace with your actual RapidAPI key
    # Map for selecting lat/long by clicking on it
    st.write("Click on the map to select a location.")
    world_map = folium.Map(location=[20, 0], zoom_start=2)

    # Use Streamlit's folium integration to show the map
    clicked_location = st_folium(world_map, width=700, height=500)

    # Print clicked_location to inspect the returned structure
    st.write("Clicked Location:", clicked_location)

    # Get latitude and longitude from the map click
    latitude = None
    longitude = None

    if clicked_location:
        if "lat" in clicked_location and "lon" in clicked_location:
            latitude = clicked_location["lat"]
            longitude = clicked_location["lon"]
            st.write(f"Latitude: {latitude}, Longitude: {longitude}")
        else:
            st.write("No location clicked yet or returned.")

    # Dropdown for selecting city and country
    city_options = [
        "Raleigh",
        "London",
        "New York",
    ]  # Replace with real data or API call
    country_options = ["US", "UK", "Canada"]  # Replace with real data or API call

    selected_city = st.selectbox("Select a City", city_options)
    selected_country = st.selectbox("Select a Country", country_options)

    # If latitude and longitude are selected from the map, use that, else use dropdowns
    if latitude and longitude:
        st.write(f"Fetching data for {selected_city}, {selected_country}...")
    else:
        # Use a mapping of cities to lat/long or fetch it from an API
        city_latitudes = {"Raleigh": 35.779, "London": 51.5074, "New York": 40.7128}
        city_longitudes = {"Raleigh": -78.638, "London": -0.1278, "New York": -74.0060}

        latitude = city_latitudes.get(
            selected_city, 35.779
        )  # Default to Raleigh if not found
        longitude = city_longitudes.get(
            selected_city, -78.638
        )  # Default to Raleigh if not found
        st.write(f"Fetching data for {selected_city}, {selected_country}...")

    # Fetch air quality data from the API using the selected lat/long
    data = fetch_air_quality_data(api_key, latitude, longitude)

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
        else:
            st.write("Missing required columns in the data!")


if __name__ == "__main__":
    main()
