import json
from flatten_json import flatten
# from pyspark.sql import SparkSession
# import pandas as pd
# from pyspark.sql.types import *
# from pyspark.sql.functions import regexp_replace, col

# # Initialize a Spark session
# spark = SparkSession.builder \
#     .appName("JSON to CSV with Defined Schema") \
#     .getOrCreate()
    
    
# stucture_details={
#   "/hardware-interface": {
#     "schema": "schema1",
#     "table": "dtdlogs"
#   },
#   "page_name2": {
#     "schema": "schema2",
#     "table": "test2"
#   }
# }


# Path to your JSON file
json_file_path = "Admin_24-1-2024- 6-50-52 pm 1 copy.json"

# Load JSON data from the file
with open(json_file_path, 'r') as file:
    json_data = json.load(file)

# Check if the loaded data is a list
if not isinstance(json_data, list):
    raise ValueError("The JSON data should be a list of JSON objects.")

# Flatten each JSON object in the list
flattened_data = [flatten(record) for record in json_data]



# # Define the schema for the DataFrame
# # You may need to customize this schema based on your actual data
# schema1 = StructType([
#     StructField("createAt", StringType(), True),
#     StructField("user", StringType(), True),
#     StructField("loginAt", StringType(), True),
#     StructField("logoutAt", StringType(), True),
#     StructField("request_event", StringType(), True),
#     StructField("request_page", StringType(), True),
#     StructField("request_action", StringType(), True),
#     StructField("request_dllCallMethod", StringType(), True),
#     StructField("response_event", StringType(), True),
#     StructField("response_data_user", StringType(), True),
#     StructField("response_data_loginAt", StringType(), True),
#     StructField("response_data_isLogin", BooleanType(), True),
#     StructField("response_data_logoutAt", StringType(), True),
#     StructField("response_data_isLogout", BooleanType(), True),
#     StructField("response_data_status", IntegerType(), True),
#     StructField("response_data_message", StringType(), True),
#     StructField("response_data_error", BooleanType(), True),
#     StructField("response_data_dllCallMethod", StringType(), True),
#     StructField("response_data_vciList", StringType(), True),
# ])

# # Define JDBC connection properties
# jdbc_url = "jdbc:mysql://127.0.0.1:3306/test"
# connection_properties = {
#     "user": "root",
#     "password": "",
#     "driver": "com.mysql.jdbc.Driver"
# }

# # Create DataFrame for each flattened JSON object and print it
# for record in flattened_data:
#     if record.get("request_page")[1:] == "hardware-interface":
#         # Ensure the record matches the schema
#         record_with_schema = {k: record.get(k) for k in schema1.fieldNames()}
#         print("record_with_schema",record_with_schema)
#         df = spark.createDataFrame([record_with_schema], schema=schema1)
#         df = df.withColumn("request_page", regexp_replace(regexp_replace(col("request_page"), "^/", ""), "-", " "))
#         #df.show(truncate=False) 
#         #df.write.jdbc(url=jdbc_url, table="dtdlogs", mode="append", properties=connection_properties)


# spark.stop()








