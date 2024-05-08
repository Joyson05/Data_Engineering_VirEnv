from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import json
import os
import sys
os.environ['PYSPARK_PYTHON'] = sys.executable #Python worker 
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable #Python driver

try: 
    # Initialize SparkSession
    spark = SparkSession.builder \
        .appName("ReadLogsToDataFrame") \
        .getOrCreate()

    # Path to the folder containing log files
    folder_path = r'D:\Data_Engineering_VirEnv\Java_Microservices_Logs\demoauth'

    # List all log files in the folder
    log_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.log')]

    # Initialize an empty list to store RDDs
    parsed_logs_rdds = []

    # Process each log file
    for log_file in log_files:
        # Read log file as text file
        log_data = spark.sparkContext.textFile(log_file)
        
        # Parse each line as JSON
        parsed_logs = log_data.map(lambda line: json.loads(line))
        
        # print(f"Contents of parsed RDD for file {log_file}:")
        # print(parsed_logs.collect())  # Collect and print all elements
        # Append parsed RDD to the list
        parsed_logs_rdds.append(parsed_logs)

    # Union all RDDs
    all_logs_rdd = spark.sparkContext.union(parsed_logs_rdds)
    print("unioned data", all_logs_rdd.collect())

    # Create DataFrame from parsed JSON data
    df = spark.createDataFrame(all_logs_rdd)

    new_columns = [col(column).alias(column.replace("@", "")) for column in df.columns]

    # Apply the new column names to the DataFrame
    df = df.select(new_columns)
    # Show DataFrame schema and sample data
    df.printSchema()
    df.show()
    # Define JDBC connection properties
    jdbc_url = "jdbc:mysql://13.232.201.238:3306/DATADB"
    connection_properties = {
        "user": "datauser",
        "password": "Data@123",
        "driver": "com.mysql.jdbc.Driver"
    }

    # Write DataFrame to MySQL using PySpark's JDBC data source
    df.write.jdbc(url=jdbc_url, table="pyspark_table", mode="append", properties=connection_properties)


    # Stop SparkSession
    spark.stop()

except Exception as e:
    # Handle specific exception related to ShutdownHookManager
    if 'ShutdownHookManager' in str(e):
        print("Error occurred in ShutdownHookManager. Ignoring...")
    else:
        # Handle other exceptions
        print("An error occurred:", e)

