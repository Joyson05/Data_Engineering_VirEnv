from kafka import KafkaConsumer
import pandas as pd
import json
import time

# Kafka broker address
bootstrap_servers = "localhost:9092"

# Kafka topic to consume data from
topic = "kafkaTest"

# Create a Kafka consumer
consumer = KafkaConsumer(topic, bootstrap_servers=bootstrap_servers,
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))

# Function to store data in MySQL
def store_to_mysql(data):
    # Assuming 'data' is a list of dictionaries where each dictionary represents a row to be inserted
    # You may need to adjust this based on the format of your Kafka messages
    df = pd.DataFrame(data)
    print(df)
    # print(df.dtypes)
    # Use sqlalchemy to store the DataFrame in MySQL
    import sqlalchemy
    from sqlalchemy import create_engine
    user = 'root'
    password = ''
    host = '127.0.0.1'
    port = 3306
    database = 'test'
    engine = create_engine(url="mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}".format(user, password, host, port, database))
    df.to_sql("pysparktable", engine, if_exists="append", index=False)


# Consume data from Kafka and store it in MySQL
data_to_store = []
for message in consumer:
    data = message.value['message']
    data_to_store.append(data)
   
    if len(data_to_store)>1:
        store_to_mysql(data_to_store)
        data_to_store = []  

if data_to_store:
    store_to_mysql(data_to_store)
