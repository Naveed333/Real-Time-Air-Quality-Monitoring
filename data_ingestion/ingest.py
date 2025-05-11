import psycopg2
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def store_data_in_postgresql(data, db_params):
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO air_quality (city, aqi, timestamp) VALUES (%s, %s, %s)
            """,
            (data["city"], data["aqi"], datetime.now()),
        )
        conn.commit()
        cursor.close()
        conn.close()
        logger.info("Data successfully stored in PostgreSQL")
    except Exception as e:
        logger.error(f"Error storing data in PostgreSQL: {e}")
