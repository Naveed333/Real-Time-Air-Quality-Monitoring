import requests
import logging

logger = logging.getLogger("producer")


def fetch_aqi(city="Lahore"):
    """
    Fetch latest AQI data for a given city using the OpenAQ API.
    """
    url = f"https://api.openaq.org/v2/latest?city={city}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Fetched AQI data for {city}")
        return data
    except requests.RequestException as e:
        logger.error(f"Failed to fetch AQI data: {e}")
        return None
