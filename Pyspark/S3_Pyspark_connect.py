from pyspark.sql import SparkSession
import boto3
import json


spark = SparkSession.builder \
    .appName("S3 Data Retrieval") \
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
list_response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix='json_files/')
# iterate over names
# for i in response.get("Contents",None):
#     print(i.get("Key",None))
    # Retrieve JSON file objects
json_files = []
for obj in list_response.get('Contents', []):
    key = obj['Key']
    if key.endswith('.log'):
        json_files.append(key)
#print("json_path",json_files)


for file_key in json_files:
    json_list= []
    get_response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
    json_content = get_response['Body'].read().decode('utf-8')
    print(f"Contents of '{file_key}':")
    print("json_content",type(json_content))
    #json_obj = json.loads(json_content)
    # Split the JSON content into lines and parse each line as JSON
    for line in json_content:
        if line.strip():  # Skip empty lines
            print(line)
            # Parse each line as JSON
            json_obj = json.loads(line)
            json_list.append(json_obj)
    # print("type", type(json_obj))
    # print(json_obj)
    print(json_list)



# Convert JSON string to PySpark DataFrame
# df = spark.read.json(spark.sparkContext.parallelize([json_content]))

# # Show the DataFrame schema and sample data
# df.printSchema()
# df.show()
