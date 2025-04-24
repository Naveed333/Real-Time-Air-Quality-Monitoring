import requests
import json
from kafka import KafkaProducer
from time import sleep

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)


def fetch_aqi():
    url = "https://api.openaq.org/v2/latest?city=Lahore"
    response = requests.get(url)
    data = response.json()
    return data


while True:
    aqi_data = fetch_aqi()
    producer.send("aqi-topic", aqi_data)
    sleep(3600)  # every hour
