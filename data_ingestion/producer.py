import requests
from kafka import KafkaProducer
import json
import random
import time
import logging

# Kafka producer setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("producer")
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",  # Kafka server address
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)


def generate_data():
    # Simulated air quality data generation
    data = {
        "timestamp": time.time(),
        "pm25": random.randint(0, 150),
        "pm10": random.randint(0, 200),
        "co": random.uniform(0, 10),
        "temperature": random.uniform(15, 30),
        "humidity": random.uniform(30, 80),
    }
    return data


# Send simulated air quality data to Kafka every 5 seconds
while True:
    air_quality_data = generate_data()
    producer.send("air-quality", air_quality_data)  # Send data to 'air-quality' topic
    print(f"Sent: {air_quality_data}")
    time.sleep(5)
