import requests
import json
from kafka import KafkaProducer
from time import sleep
import logging

from api_client import fetch_aqi

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("producer")

# Kafka configuration (for running from host)
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)


def main():
    while True:
        data = fetch_aqi()
        if data:
            try:
                producer.send("aqi-topic", data)
                logger.info("Sent data to Kafka topic 'aqi-topic'")
            except Exception as e:
                logger.error(f"Failed to send data to Kafka: {e}")
        else:
            logger.warning("No data to send")

        sleep(3600)  # Wait for 1 hour before next fetch


if __name__ == "__main__":
    main()
