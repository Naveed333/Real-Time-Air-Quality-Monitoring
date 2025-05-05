import requests


def get_air_quality_data(city="Lahore"):
    url = f"https://api.openaq.org/v2/latest?city={city}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to fetch air quality data: {e}")
        return {}
