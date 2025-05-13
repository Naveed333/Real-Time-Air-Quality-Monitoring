from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
import time
from pyspark.sql.types import (
    StructType,
    StructField,
    FloatType,
    StringType,
    IntegerType,
    DoubleType,
)
from influxdb_client import InfluxDBClient, Point, WriteOptions

# Initialize Spark session with Kafka support
spark = SparkSession.builder.appName("AirQualityStreaming").getOrCreate()

# Define schema for air quality data
schema = StructType(
    [
        StructField("timestamp", FloatType(), True),
        StructField("pm25", FloatType(), True),  # PM2.5 as a float
        StructField("pm10", FloatType(), True),  # PM10 as a float
        StructField("co", FloatType(), True),  # CO as a float
        StructField("temperature", FloatType(), True),  # Temperature as a float
        StructField("humidity", FloatType(), True),  # Humidity as a float
        StructField("latitude", FloatType(), True),  # Latitude as a float
        StructField("longitude", FloatType(), True),  # Longitude as a float
    ]
)

spark.sparkContext.setLogLevel("WARN")


# InfluxDB Client setup
influx_client = InfluxDBClient(
    url="http://localhost:8086",
    # token="g6QijRA4AJ9KDRkv7nEX0qKBf-DvS2cqYDVEpBJ4ZT1OFtD7obXFD8GCI-ETIgtE6IgPBPmjriDFOl_CJuHf3A==",
    # token="c6n-pd3uqy-NlNwUZiQhniXHrn34MWp9n-ULoYKXbr2DbvTCiDOTNIBypws5kPTkmk9ptHKWeSrNI-MtQKwsWQ==",
    # token="vawI7T7U2qpjcrVudNtR5s_WE0FhCiaaBFxxw2PTNOetinCwRAh4cAniWtNUmxgVvJ-LwTnBnimkEiO7A0vyEA==",
    token="xhk1y3Yx70sTEQ5iNhEc_UgqkLMlLMDA6QU3XBizJT-U3iWaWbCjHwzpzg1OHHGqHFuSEdgpVHaVb0XIS7IUsQ==",
    org="de",
)
write_api = influx_client.write_api(write_options=WriteOptions(batch_size=1))


# # Read data from Kafka topic 'air-quality'
# air_quality_stream = (
#     spark.readStream.format("kafka")
#     .option("kafka.bootstrap.servers", "localhost:9092")
#     .option("subscribe", "air_quality")
#     .load()
# )

# # Deserialize the JSON data
# air_quality_df = (
#     air_quality_stream.selectExpr("CAST(value AS STRING)")
#     .select(from_json("value", schema).alias("data"))
#     .select("data.*")  # Flatten the nested structure
# )

# # Check if the data has all the required columns and clean it
# # air_quality_df = air_quality_df.filter(
# #     col("pm25").isNotNull() & col("pm10").isNotNull() & col("co").isNotNull()
# # )

# # Output data to the console (for testing)
# query = air_quality_df.writeStream.outputMode("append").format("console").start()
# query.awaitTermination()


# Kafka Consumer to read from 'air-quality' topic
while True:
    df = (
        spark.read.format("kafka")
        .option("kafka.bootstrap.servers", "localhost:9092")
        .option("subscribe", "air_quality")
        .option("startingOffsets", "earliest")
        .load()
    )

    if df.rdd.isEmpty():
        print("No new data. Waiting...")
    else:
        # Parse the incoming JSON data
        parsed = (
            df.selectExpr("CAST(value AS STRING) as json_string")
            .select(from_json(col("json_string"), schema).alias("data"))
            .select("data.*")
        )

        # Data Quality Checks (Ensure all required fields are non-null)
        parsed = parsed.filter(
            col("timestamp").isNotNull()
            & col("pm25").isNotNull()
            & col("pm10").isNotNull()
            & col("co").isNotNull()
            & col("temperature").isNotNull()
            & col("humidity").isNotNull()
        )

        # Handle the data and send it to InfluxDB
        for row in parsed.collect():
            # Create a point for InfluxDB
            point = (
                Point("air_quality_data")
                .tag("sensor_id", row["timestamp"])
                .field("pm25", int(row["pm25"]))
                .field("pm10", int(row["pm10"]))
                .field("co", float(row["co"]))
                .field("temperature", float(row["temperature"]))
                .field("humidity", float(row["humidity"]))
                .time(time.time_ns())
            )

            # Write the data to InfluxDB
            write_api.write(bucket="air_quality_metrics", org="de", record=point)

        print("Data successfully written to InfluxDB.")

    time.sleep(5)
