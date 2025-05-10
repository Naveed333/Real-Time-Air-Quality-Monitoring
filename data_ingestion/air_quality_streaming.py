from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, FloatType, IntegerType

# Initialize Spark session with Kafka support
spark = (
    SparkSession.builder.appName("AirQualityStreaming")
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2")
    .getOrCreate()
)

# Define schema for air quality data
schema = StructType(
    [
        StructField("timestamp", FloatType(), True),
        StructField("pm25", IntegerType(), True),
        StructField("pm10", IntegerType(), True),
        StructField("co", FloatType(), True),
        StructField("temperature", FloatType(), True),
        StructField("humidity", FloatType(), True),
    ]
)

# Read data from Kafka topic (air-quality)
air_quality_stream = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "air-quality")
    .load()
)

# Deserialize the JSON data
air_quality_df = (
    air_quality_stream.selectExpr("CAST(value AS STRING)")
    .select(from_json("value", schema).alias("data"))
    .select("data.*")
)

# Filter data: PM2.5 level > 100 as an example
threshold = 100
filtered_data = air_quality_df.filter(col("pm25") > threshold)

# Write filtered data to the console
query = filtered_data.writeStream.outputMode("append").format("console").start()

query.awaitTermination()
