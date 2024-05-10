import time
import json
from kafka import KafkaProducer
import requests

# Kafka broker(s) address
bootstrap_servers = "127.0.0.1:9092"
api_url = 'http://127.0.0.1:5000/'
# Kafka topic to send data to
topic = "demo-topic"

# Create Kafka producer
producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                         value_serializer=lambda v: json.dumps(v).encode("utf-8"))

# Function to generate streaming data
def generate_data():
    # count = 1
    while True:
        response = requests.get(api_url)
        api_data = response.json() 
        producer.send(topic, value=api_data)
        print(f"Produced: {api_data}") 
        time.sleep(1)

        # data = {"message":count}
        # producer.send(topic, value=data)
        # print(f"Produced: {data}")
        # count += 1
        # time.sleep(2)

# Start generating data
if __name__ == "__main__":
    generate_data()