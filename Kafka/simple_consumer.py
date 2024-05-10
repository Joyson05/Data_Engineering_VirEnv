from kafka import KafkaConsumer
import json
# Kafka broker address
bootstrap_servers = "localhost:9092"

# Kafka topic to consume data from
topic = "kafka_test"

# Create a Kafka consumer
consumer = KafkaConsumer(topic,
                         bootstrap_servers=bootstrap_servers,
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))

# Consume data from Kafka topic
for message in consumer:
    # Each message is represented as a ConsumerRecord object
    # The actual message value can be accessed using the 'value' attribute
    message_value = message.value['message']
    print(f"Received: {message_value}")