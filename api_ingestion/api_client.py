import requests


def get_air_quality_data(city="Lahore"):
    url = f"https://api.openaq.org/v2/latest?city={city}"
    return requests.get(url).json()
