import boto3
from datetime import datetime, timedelta



# AWS credentials
aws_access_key_id = 'AKIAU6GDWNO4FL3DSEF5'
aws_secret_access_key = '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'
region_name = 'ap-south-1'
bucket_name = 'demo-bucket-joy'

s3_client = boto3.client('s3',
                        aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key,
                        region_name=region_name)



# Get the list of files in the specified S3 bucket and folder
response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

# Get today's date and calculate the date for "yesterday"
today = datetime.now()
yesterday = today - timedelta(days=1)

# Filter files that were uploaded yesterday
files = []
for obj in response.get('Contents', []):
    last_modified = obj['LastModified']
    if yesterday.date() == last_modified.date():
        files.append(obj['Key'])

# Check if we have found any files
if not files:
    print("No files found that were uploaded yesterday.")
else:
    print(f"Files found: {files}")
