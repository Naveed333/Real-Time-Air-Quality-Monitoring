import requests
import json
from kafka import KafkaProducer
import streamlit as st
import time
from geopy.geocoders import Nominatim  # Import geopy for geocoding
from geopy.exc import GeocoderUnavailable

# Initialize geolocator
geolocator = Nominatim(user_agent="air_quality_app")


def get_lat_long(city, country):
    try:
        location = geolocator.geocode(f"{city}, {country}", timeout=10)
        if location:
            return location.latitude, location.longitude
        else:
            st.error(f"Could not find location for {city}, {country}")
            return None, None
    except GeocoderUnavailable:
        st.error("Geocoding service is unavailable. Please try again later.")
        return None, None


def fetch_air_quality_data(api_key, city, country):
    # Get dynamic latitude and longitude
    latitude, longitude = get_lat_long(city, country)

    if latitude is None or longitude is None:
        return None

    url = "https://air-quality.p.rapidapi.com/history/airquality"
    querystring = {"lat": str(latitude), "lon": str(longitude)}

    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "air-quality.p.rapidapi.com",
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            data = response.json()

            # If the API response contains air quality data
            if "data" in data:
                # Add latitude and longitude to each air quality record
                for record in data["data"]:
                    record["latitude"] = latitude
                    record["longitude"] = longitude

            return data
        elif response.status_code == 429:  # Handle rate limiting
            st.error("Too many requests. Please try again later.")
            time.sleep(120)  # Wait for 120 seconds before retrying
            return fetch_air_quality_data(api_key, city, country)  # Retry the request
        else:
            st.error(f"Error fetching air quality data: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error fetching air quality data: {str(e)}")
        return None
