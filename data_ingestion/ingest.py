import requests
# import psycopg2
from datetime import datetime
# import logging
from logging import getLogger

logger = getLogger(__name__)


def fetch_air_quality_data(api_key, latitude, longitude):
    url = "https://air-quality.p.rapidapi.com/history/airquality"

    querystring = {"lon": str(longitude), "lat": str(latitude)}

    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "air-quality.p.rapidapi.com",
    }

    try:
        # Make the GET request to the API
        response = requests.get(url, headers=headers, params=querystring)

        # Check if the response is successful
        response.raise_for_status()

        # Log the success
        logger.info(
            f"Successfully fetched air quality data for lat: {latitude}, lon: {longitude}"
        )

        # Print the response to check its structure
        print(response.json())  # This will print the response for inspection

        # Return the JSON data from the response
        return response.json()

    except requests.exceptions.RequestException as e:
        # Log the error if any
        logger.error(f"Error fetching air quality data: {e}")
        return None


# # Store the fetched data into PostgreSQL database
# def store_data_in_postgresql(data, db_params):
#     try:
#         conn = psycopg2.connect(**db_params)
#         cursor = conn.cursor()
#         cursor.execute(
#             """
#             INSERT INTO air_quality (city, aqi, timestamp) VALUES (%s, %s, %s)
#         """,
#             (data["city"], data["aqi"], datetime.now()),
#         )
#         conn.commit()
#         cursor.close()
#         conn.close()
#         logger.info("Data successfully stored in PostgreSQL")
#     except Exception as e:
#         logger.error(f"Error storing data in PostgreSQL: {e}")
