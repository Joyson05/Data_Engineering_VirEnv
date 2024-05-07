from minio import Minio
import os
os.environ["MINIO_CACHE_DRIVES"] = ""

client = Minio("127.0.0.1:9000",
    access_key="p9kFpIaX2QmO9c7IjZmJ",
    secret_key="go7wJrH1UWwOWvZD6J8IcvdsxaCX34cwyBVyxlj9",
    secure=False
)

bucket_name = "demo"
destination_file = "doc.txt"
source_file = r"D:\Minio\minio document.txt"  # Note the 'r' prefix to treat it as a raw string

client.fput_object(bucket_name, destination_file, source_file)    #write object
# response = client.get_object(                                      #read object
#     bucket_name,
#     "PMS_2024.txt",  # Use the gateway port (default: 9001)
# )
# object_content = response.read()
# print(object_content.decode())
