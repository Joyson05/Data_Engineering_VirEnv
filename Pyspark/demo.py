import json
from flatten_json import flatten

# Path to your JSON file
json_file_path = r"D:\Data_Engineering_VirEnv\dtd_logs\dtdlogs_demo.json"
# Path to your flattened JSON file
flattened_json_file_path = "flattened_json_file.json"

# Load JSON data from the file
with open(json_file_path, 'r') as file:
    json_data = json.load(file)

# Check if the loaded data is a list
if not isinstance(json_data, list):
    raise ValueError("The JSON data should be a list of JSON objects.")

# Flatten each JSON object in the list
flattened_data = [flatten(record) for record in json_data]

# # Save the flattened data to a new file
with open(flattened_json_file_path, 'w') as file:
    json.dump(flattened_data, file, indent=4)

# Print the flattened data to console
for record in flattened_data:
    print(record)
