import json
import os

def main():
    initial_data={}
    initial_data["users"]=[{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
    # Write the initial data to a JSON file
    # with open("data.json", "w") as json_file:

    if os.path.exists("data.json"):
        with open("data.json", "r") as json_file:
            existing_data = json.load(json_file)
        # Add new content to the JSON data
        new_user = {"id": 3, "name": "Charlie"}
        existing_data["users"].append(new_user)

        # Write the updated data back to the JSON file
        with open("data.json", "w") as json_file:
            json.dump(existing_data, json_file, indent=4)
            print("Content added and appended to the JSON file.")
    else:
        # Write the initial data to a JSON file
        with open("data.json", "w") as json_file:
            json.dump(initial_data, json_file, indent=4)
            
    return "File Added"

main()
            

