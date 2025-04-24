from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.appName("AQIProcessor").getOrCreate()
df = spark.read.json("s3a://air-quality/raw/")

clean_df = df.dropna().filter(col("value") > 0)
clean_df.write.mode("overwrite").parquet("s3a://air-quality/processed/")
