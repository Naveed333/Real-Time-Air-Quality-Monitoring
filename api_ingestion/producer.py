import requests
import json
from kafka import KafkaProducer
from time import sleep
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("producer")

producer = KafkaProducer(
    bootstrap_servers="kafka:9092",
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


if __name__ == "__main__":
    while True:
        data = fetch_aqi()
        if data:
            producer.send("aqi-topic", data)
            logger.info("Data sent to Kafka topic 'aqi-topic'")
        sleep(3600)
