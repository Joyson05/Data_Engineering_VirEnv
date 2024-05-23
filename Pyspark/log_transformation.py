import os
import sys
import json
# import boto3
import schema
from flatten_json import flatten
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import regexp_replace, col

# os.environ['PYSPARK_PYTHON'] = sys.executable #Python worker 
# os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable #Python driver

# Initialize a Spark session
spark = SparkSession.builder \
    .appName("JSON to CSV with Defined Schema") \
    .getOrCreate()

# # AWS credentials
# aws_access_key_id = 'AKIAU6GDWNO4FL3DSEF5'
# aws_secret_access_key = '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'
# region_name = 'ap-south-1'
# bucket_name = 'demo-bucket-joy'


# s3_client = boto3.client('s3',
#                         aws_access_key_id=aws_access_key_id,
#                         aws_secret_access_key=aws_secret_access_key,
#                         region_name=region_name)

# Define JDBC connection properties
jdbc_url = "jdbc:mysql://127.0.0.1:3306/dtdlogs"
connection_properties = {
    "user": "root",
    "password": "",
    "driver": "com.mysql.jdbc.Driver"
}


# Path to your JSON file
json_file_path = r"D:\Data_Engineering_VirEnv\dtd_logs\dtdlogs_demo.json"

# Load JSON data from the file
with open(json_file_path, 'r') as file:
    json_data = json.load(file)
# print("json_data",json_data)
# for item in json_data[0]:
#     print("item_vin",item["vin"])

# Flatten each JSON object in the list
flattened_data = [flatten(record) for record in json_data]
# Export the flattened data as .json
output_file_path = 'flattened_data.json'
with open(output_file_path, 'w') as outfile:
    json.dump(flattened_data, outfile, indent=4)



# Create DataFrame for each flattened JSON object wrt page
for i, record in enumerate(flattened_data):
    print(i)
    # vechile-summary page..........
    if record.get("request_page") == "/vechile-summary":
        # Ensure the record matches the schema
        base_record_vechicle_summary = {k: record.get(k) for k in schema.vechicle_summary_base_schema.fieldNames()}
        df = spark.createDataFrame([base_record_vechicle_summary], schema=schema.vechicle_summary_base_schema)
        df = df.withColumn("request_page", regexp_replace(regexp_replace(col("request_page"), "^/", ""), "-", " "))
        df.write.jdbc(url=jdbc_url, table="vechicle_summary_base_record", mode="append", properties=connection_properties)
        
        if record.get("request_dllCallMethod") == "ECU coordinates":
            response_record_coordinates_vechicle_summary = {k: record.get(k) for k in schema.vechicle_summary_response_coordinates.fieldNames()}
            df = spark.createDataFrame([response_record_coordinates_vechicle_summary], schema=schema.vechicle_summary_response_coordinates)
            df.write.jdbc(url=jdbc_url, table="vechicle_summary_response_coordinates", mode="append", properties=connection_properties)
            
        if record.get("request_dllCallMethod") == "DTC list":
            json_data_filtered=json_data[i]
            print("json_data_filtered",json_data_filtered)
            vin = json_data_filtered["vin"]
            data=json_data_filtered["response"]["data"]["data"]
            print("data",data)
            for entry in data:
                entry["vin"] = vin
            for j in data:
                response_record_dtclist_vechicle_summary = {k: j.get(k) for k in schema.vechicle_summary_response_dtclist.fieldNames()}
                df = spark.createDataFrame([response_record_dtclist_vechicle_summary], schema=schema.vechicle_summary_response_dtclist)
                df.write.jdbc(url=jdbc_url, table="vechicle_summary_response_dtclist", mode="append", properties=connection_properties)
            
    # fault-management page..........used the schema of vechile-summary page         
    if record.get("request_page") == "/fault-management":
        # Ensure the record matches the schema
        base_record_fault_management = {k: record.get(k) for k in schema.vechicle_summary_base_schema.fieldNames()}
        df = spark.createDataFrame([base_record_fault_management], schema=schema.vechicle_summary_base_schema)
        df = df.withColumn("request_page", regexp_replace(regexp_replace(col("request_page"), "^/", ""), "-", " "))
        df.write.jdbc(url=jdbc_url, table="fault_management_base_record", mode="append", properties=connection_properties)
        table_scan="fault_management_scan_ecu"
        table_clear="fault_management_clear_dtc" 
        json_data_filtered=json_data[i]    
        #for item in json_data:
        vin = json_data_filtered["vin"]
        data=json_data_filtered["response"]["data"]["data"]
        for entry in data:
            entry["vin"] = vin
        for j in data:
            response_record_dtclist_fault_management = {k: j.get(k) for k in schema.vechicle_summary_response_dtclist.fieldNames()}
            df = spark.createDataFrame([response_record_dtclist_fault_management], schema=schema.vechicle_summary_response_dtclist)
            df.write.jdbc(url=jdbc_url, table=table_scan if record.get("request_action") == "scan ECU" else table_clear, mode="append", properties=connection_properties)



spark.stop()



#need to create table schema for fault management page in db






