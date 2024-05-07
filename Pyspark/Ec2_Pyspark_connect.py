import boto3
import json
from pyspark.sql import SparkSession
import os
import sys
import pandas as pd

os.environ['PYSPARK_PYTHON'] = sys.executable #Python worker 
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable #Python driver

# spark = SparkSession.builder \
#     .appName("S3 Data Retrieval") \
#     .getOrCreate()
    

folder_path = r'D:\Data_Engineering_VirEnv\Java_Microservices_Logs\demoauth'
json_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.log')]

print(json_files)
df = pd.read_json(json_files, lines=True)

df=spark.createDataFrame(df)

# data = spark.read.text(r"D:\Data_Engineering_VirEnv\Java_Microservices_Logs\authService\authService.2024-04-16.0.log")


# # Process the data
# data.show()

# # Stop SparkSession
# spark.stop()
