import boto3
from boto3 import client
import json
from pyspark.sql import SparkSession
import os
import sys

os.environ['PYSPARK_PYTHON'] = sys.executable #Python worker 
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable #Python driver

try:
    # Initialize SparkSession
    spark = SparkSession.builder \
        .appName("LogDataToDataFrame") \
        .getOrCreate()
        
    # AWS credentials
    aws_access_key_id = 'AKIAU6GDWNO4FL3DSEF5'
    aws_secret_access_key = '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'
    region_name = 'ap-south-1'
    bucket_name = 'demo-bucket-joy'

    s3_client = boto3.client('s3',
                            aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key,
                            region_name=region_name)


    # Get list objects in the S3 bucket
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix='json_files/')
    #print(response)
    # iterate over names
    for i in response.get("Contents",None):
        print(i.get("Key",None))
    # Retrieve JSON file objects
    json_files = []
    for obj in response.get('Contents', []):
        key = obj['Key']
        #print("key",key)
        if key.endswith('.json'):
            json_files.append(key)
    print(json_files)


    for file_key in json_files:
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        json_content = response['Body'].read().decode('utf-8')
        # print(f"Contents of '{file_key}':")
        # print(type(json_content))
        
    json_list=[]        
    for line in json_content.strip().split('\n'):
        json_list.append(json.loads(line))

    # Create PySpark DataFrame from the list of dictionaries
    df = spark.createDataFrame(json_list)

    # Show DataFrame schema and sample data
    df.printSchema()
    df.show()

    # Stop SparkSession
    spark.stop()
    
except Exception as e:
    # Handle specific exception related to ShutdownHookManager
    if 'ShutdownHookManager' in str(e):
        print("Error occurred in ShutdownHookManager. Ignoring...")
    else:
        # Handle other exceptions
        print("An error occurred:", e)



