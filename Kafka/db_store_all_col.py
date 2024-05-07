from kafka import KafkaConsumer
import pandas as pd
import json
import time
# Kafka broker address
bootstrap_servers = "127.0.0.1:9092"

# Kafka topic to consume data from
topic = "demo-topic"

# Create a Kafka consumer
consumer = KafkaConsumer(topic, bootstrap_servers=bootstrap_servers,
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))

def store_data(data):
    df = pd.DataFrame()
    df["Speed"] = None
    df["Steering angle"] = None
    df["Trip"] = None
    df["Weather"] = None
    df["accelX"] = None
    df["accelY"] = None
    df["accelZ"] = None
    df["gyroX"] = None
    df["gyroY"] = None
    df["gyroZ"] = None
    df["timestamp"] = None
    df.loc[len(df)] = data
    print(df) 

    #db store
    import sqlalchemy
    from sqlalchemy import create_engine
    user = 'root'
    password = ''
    host = '127.0.0.1'
    port = 3306
    database = 'test'
    engine = create_engine(url="mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}".format(user, password, host, port, database))
    df.to_sql("pysparktable", engine, if_exists="append", index=False)


col=["Speed","Steering angle","Trip","Weather","accelX","accelY","accelZ","gyroX","gyroY","gyroZ","timestamp"]
while True:
    time.sleep(1)
    for message in consumer:
        data=[]
        for i in col:
            data.append(message.value[i])
        print(data)
        store_data(data)
# print(consumer)