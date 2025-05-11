import requests
import json
from kafka import KafkaProducer
import streamlit as st
import time


# def fetch_air_quality_data(city="Lahore"):
#     url = f"https://api.openaq.org/v2/latest?city={city}"
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         return response.json()
#     except requests.RequestException as e:
#         print(f"Failed to fetch air quality data: {e}")
#         return {}
def fetch_air_quality_data(api_key, latitude, longitude):
    url = "https://air-quality.p.rapidapi.com/history/airquality"

    querystring = {"lon": str(longitude), "lat": str(latitude)}

    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "air-quality.p.rapidapi.com",
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:  # Handle rate limiting
            st.error("Too many requests. Please try again later.")
            time.sleep(120)  # Wait for 60 seconds before retrying
            return fetch_air_quality_data(
                api_key, latitude, longitude
            )  # Retry the request
        else:
            st.error(f"Error fetching air quality data: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error fetching air quality data: {str(e)}")
        return None


def send_data_to_kafka(data, topic="air-quality"):
    producer = KafkaProducer(
        bootstrap_servers="localhost:9092",
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )
    producer.send(topic, data)
    producer.flush()
    print(f"Data sent to Kafka topic '{topic}'")
