import requests

# import psycopg2
from datetime import datetime

# import logging
from logging import getLogger

logger = getLogger(__name__)

import time
import requests
import streamlit as st


def fetch_air_quality_data(api_key, latitude, longitude):
    url = "https://air-quality.p.rapidapi.com/history/airquality"

    querystring = {"lon": str(longitude), "lat": str(latitude)}

    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "air-quality.p.rapidapi.com",
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:  # Handle rate limiting
            st.error("Too many requests. Please try again later.")
            time.sleep(120)  # Wait for 60 seconds before retrying
            return fetch_air_quality_data(
                api_key, latitude, longitude
            )  # Retry the request
        else:
            st.error(f"Error fetching air quality data: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error fetching air quality data: {str(e)}")
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
