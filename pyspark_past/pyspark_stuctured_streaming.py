from pyspark.sql import SparkSession

# Start a Spark session
spark = SparkSession.builder \
    .appName("MySQL Structured Streaming") \
    .getOrCreate()

# Define JDBC connection properties
jdbc_url = "jdbc:mysql://127.0.0.1:3306/test"
connection_properties = {
    "user": "root",
    "password": "",
    "driver": "com.mysql.jdbc.Driver"
}

# Define the streaming query to read data from MySQL
streaming_data = spark.readStream \
    .format("jdbc") \
    .option("url", jdbc_url) \
    .option("dbtable", "pysparktable") \
    .option("user", connection_properties["user"]) \
    .option("password", connection_properties["password"]) \
    .option("driver", connection_properties["driver"]) \
    .load()

# Define your stream processing logic
# For example, you can perform transformations and write to an output sink
# Here, we just print the data to the console
query = streaming_data.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

# Wait for the streaming query to terminate (you can also use query.awaitTermination())
query.awaitTermination()
