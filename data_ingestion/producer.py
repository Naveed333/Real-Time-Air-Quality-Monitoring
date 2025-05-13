import sys
import os
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import requests
from kafka import KafkaProducer

# from prometheus_client import Counter, start_http_server
import json
import time
import logging
from data_ingestion.api_client import fetch_air_quality_data

# start_http_server(8000)
# vehicle_counts = Counter(
#     "vehicle_count_total",
#     "Total number of vehicle count",
#     ["sensor_id", "congestion_level"],
# )
# Kafka producer setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("producer")
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",  # Kafka server address
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)


def generate_data_from_api(api_key, city, country):
    data = fetch_air_quality_data(api_key, city, country)
    if data and "data" in data:
        air_quality_data = {
            "timestamp": time.time(),
            "pm25": data["data"][0][
                "pm25"
            ],  # Assuming "data" contains a list of air quality records
            "pm10": data["data"][0]["pm10"],
            "co": data["data"][0]["co"],
            "temperature": data["data"][0]["temperature"],
            "humidity": data["data"][0]["humidity"],
            "city": city,
            "country": country,
        }
        return air_quality_data
    else:
        return None


# Example usage with dynamic city and country
api_key = "e19e6cb107mshaa406fe397a20abp162c3cjsn670651231384"  # Replace with your actual RapidAPI key
# api_key = "89307e48a2msh4d3b023c0ca78abp19417fjsnf0868fff2816"  # Replace with your actual RapidAPI key
# You can change the city and country dynamically
city = "Raleigh"  # Example city
country = "US"  # Example country

# Send real air quality data to Kafka every 5 seconds
while True:
    # air_quality_data = generate_data_from_api(api_key, city, country)
    locations = {
        "United States": ["New York", "Los Angeles", "Chicago", "Houston", "Miami"],
        "Canada": ["Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa"],
        "Mexico": ["Mexico City", "Guadalajara", "Monterrey", "Cancun", "Puebla"],
        "United Kingdom": [
            "London",
            "Manchester",
            "Birmingham",
            "Edinburgh",
            "Liverpool",
        ],
        "Germany": ["Berlin", "Munich", "Frankfurt", "Hamburg", "Stuttgart"],
        "France": ["Paris", "Lyon", "Marseille", "Toulouse", "Nice"],
        "China": ["Beijing", "Shanghai", "Guangzhou", "Shenzhen", "Chengdu"],
        "India": ["New Delhi", "Mumbai", "Bangalore", "Kolkata", "Chennai"],
        "Japan": ["Tokyo", "Osaka", "Kyoto", "Yokohama", "Sapporo"],
        "South Africa": [
            "Cape Town",
            "Johannesburg",
            "Pretoria",
            "Durban",
            "Port Elizabeth",
        ],
        "Brazil": ["São Paulo", "Rio de Janeiro", "Brasília", "Salvador", "Fortaleza"],
    }
    country = random.choice(
        list(locations.keys())
    )  # Randomly select a country from the list
    city = random.choice(locations[country])  # Select a city from the chosen country

    air_quality_data = {
        "timestamp": time.time(),
        "pm25": random.randint(0, 150),  # PM2.5 values can range from 0 to 150 µg/m³
        "pm10": random.randint(0, 200),  # PM10 values can range from 0 to 200 µg/m³
        "co": random.uniform(0, 9),  # CO levels typically range from 0 to 9 ppm
        "temperature": random.uniform(
            15, 35
        ),  # Temperature in Celsius, realistic range (15°C to 35°C)
        "humidity": random.uniform(30, 80),  # Humidity in percentage (30% to 80%)
        "country": country,
        "city": city,  # City name for context
        "aqi": random.randint(0, 300),  # AQI (Air Quality Index), realistic range
    }

    if air_quality_data:
        producer.send("air_quality", air_quality_data)
        logger.info(f"Sent: {air_quality_data}")
    else:
        logger.error("Failed to fetch or process air quality data")

    time.sleep(5)
