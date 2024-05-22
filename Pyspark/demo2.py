import json
import schema
from flatten_json import flatten
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import regexp_replace, col


# Initialize a Spark session
spark = SparkSession.builder \
    .appName("JSON to CSV with Defined Schema") \
    .getOrCreate()
    
# Define JDBC connection properties
jdbc_url = "jdbc:mysql://127.0.0.1:3306/test"
connection_properties = {
    "user": "root",
    "password": "",
    "driver": "com.mysql.jdbc.Driver"
}


# Path to your JSON file
json_file_path = r"D:\Data_Engineering_VirEnv\Pyspark\Admin_24-1-2024- 6-50-52 pm 1 copy.json"

# Load JSON data from the file
with open(json_file_path, 'r') as file:
    json_data = json.load(file)

# Flatten each JSON object in the list
flattened_data = [flatten(record) for record in json_data]


# Create DataFrame for each flattened JSON object wrt page
for record in flattened_data:
    # vechile-summary page..........
    if record.get("request_page") == "/vechile-summary":
        # Ensure the record matches the schema
        base_record_vechicle_summary = {k: record.get(k) for k in schema.vechicle_summary_base_schema.fieldNames()}
        df = spark.createDataFrame([base_record_vechicle_summary], schema=schema.vechicle_summary_base_schema)
        df = df.withColumn("request_page", regexp_replace(regexp_replace(col("request_page"), "^/", ""), "-", " "))
        df.write.jdbc(url=jdbc_url, table="base_record_vechicle_summary", mode="append", properties=connection_properties)
        
        if record.get("request_dllCallMethod")== "ECU coordinates":
            response_record_coordinates_vechicle_summary = {k: record.get(k) for k in schema.vechicle_summary_response_coordinates.fieldNames()}
            df = spark.createDataFrame([response_record_coordinates_vechicle_summary], schema=schema.vechicle_summary_response_coordinates)
            df.write.jdbc(url=jdbc_url, table="response_coordinates_vechicle_summary", mode="append", properties=connection_properties)
            
        if record.get("request_dllCallMethod")== "DTC list":
            for item in json_data:
                vin = item["vin"]
                data=item["response"]["data"]["data"]
                for entry in data:
                    entry["vin"] = vin
                for i in data:
                    response_record_dtclist_vechicle_summary = {k: i.get(k) for k in schema.vechicle_summary_response_dtclist.fieldNames()}
                    df = spark.createDataFrame([response_record_dtclist_vechicle_summary], schema=schema.vechicle_summary_response_dtclist)
                    df.write.jdbc(url=jdbc_url, table="response_dtclist_vechicle_summary", mode="append", properties=connection_properties)
            
    # fault-management page..........        
    if record.get("request_page") == "/fault-management":
        # Ensure the record matches the schema
        base_record_fault_management = {k: record.get(k) for k in schema.vechicle_summary_base_schema.fieldNames()}
        df = spark.createDataFrame([base_record_fault_management], schema=schema.vechicle_summary_base_schema)
        df = df.withColumn("request_page", regexp_replace(regexp_replace(col("request_page"), "^/", ""), "-", " "))
        df.write.jdbc(url=jdbc_url, table="dtdlogs", mode="append", properties=connection_properties)
        
        if record.get("request_dllCallMethod")== "ECU coordinates":
            response_record_coordinates_fault_management = {k: record.get(k) for k in schema.vechicle_summary_response_coordinates.fieldNames()}
            df = spark.createDataFrame([response_record_coordinates_fault_management], schema=schema.vechicle_summary_response_coordinates)
            df.write.jdbc(url=jdbc_url, table="response_coordinates_vechicle_summary", mode="append", properties=connection_properties)
               
        if record.get("request_dllCallMethod")== "DTC list":
            for item in json_data:
                vin = item["vin"]
                data=item["response"]["data"]["data"]
                for entry in data:
                    entry["vin"] = vin
                for i in data:
                    response_record_dtclist_fault_management = {k: i.get(k) for k in schema.vechicle_summary_response_dtclist.fieldNames()}
                    df = spark.createDataFrame([response_record_dtclist_fault_management], schema=schema.vechicle_summary_response_dtclist)
                    df.write.jdbc(url=jdbc_url, table="response_dtclist_vechicle_summary", mode="append", properties=connection_properties)
    


spark.stop()



#need to create table schema for fault management page in db






