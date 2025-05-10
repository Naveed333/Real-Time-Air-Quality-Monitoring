import requests
from kafka import KafkaProducer
import json
import random
import time
from time import sleep
import logging

# Kafka producer setup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("producer")
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)


def fetch_aqi():
    url = "https://api.openaq.org/v2/latest?city=Lahore"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching AQI data: {e}")
        return None


# Generate simulated air quality data
def generate_data():
    data = {
        "timestamp": time.time(),
        "pm25": random.randint(0, 150),  # PM2.5 level
        "pm10": random.randint(0, 200),  # PM10 level
        "co": random.uniform(0, 10),  # CO concentration
        "temperature": random.uniform(15, 30),
        "humidity": random.uniform(30, 80),
    }
    return data


# Sending data to Kafka
while True:
    # data = fetch_aqi()
    # if data:
    #         producer.send("aqi-topic", data)
    #         logger.info("Data sent to Kafka topic 'aqi-topic'")
    # sleep(3600)

    air_quality_data = generate_data()
    producer.send("air-quality", air_quality_data)
    print(f"Sent: {air_quality_data}")
    time.sleep(5)  # Send data every 5 seconds
