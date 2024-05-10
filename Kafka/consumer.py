from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StringType, StructType, StructField

# Create SparkSession
spark = SparkSession.builder \
    .appName("KafkaStreamingConsumer") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.13:3.4.1") \
    .getOrCreate()

# Kafka broker(s) address
brokers = "localhost:9092"

# Kafka topic to consume data from
topic = "kafka_test"

# Define the schema for the Kafka message value
schema = StructType([StructField("message", StringType(), nullable=True)])

# Read streaming data from Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", brokers) \
    .option("subscribe", topic) \
    .load()

# Convert Kafka value from bytes to JSON string
df = df.selectExpr("CAST(value AS STRING) AS value")

# Parse the JSON string as a DataFrame
df = df.select(from_json(df.value, schema).alias("data"))
df.show()
# print(df)
# Select the "message" field and display the streaming data
query = df.select("data.message") \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

# Start the streaming query
query.awaitTermination()
