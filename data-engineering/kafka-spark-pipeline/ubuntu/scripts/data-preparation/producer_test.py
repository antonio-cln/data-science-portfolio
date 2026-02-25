#!/usr/bin/env python3

# Packages import
import sys
import time
import pandas as pd
from kafka import KafkaProducer

# Bootstrap servers variable definition
BOOTSTRAP_SERVERS = [f"127.0.0.1:{9092 + 2*i}" for i in range(int(sys.argv[1]))]

# Error management
def error_callback(exc):
    raise Exception(f"Error while sending data to kafka: {str(exc)}")
    
# Producer creation
def write_to_kafka(topic_name, messages, labels):
    count = 0
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
    for data in range(5000):
        producer.send(topic_name,
                    key=labels.iat[data].encode('utf-8'),
                    value=messages.iat[data, 0].encode('utf-8')).add_errback(error_callback)
        count += 1
        time.sleep(0.1)
        print(f"Wrote a message into topic: {topic_name}")
    producer.flush()
    
# Data loading
test_df = pd.read_parquet("test_df.parquet")

# Splitting into explanatory variables and response variable
x_test_df = test_df.drop(['Label'], axis=1)
y_test_df = test_df['Label']

# Sending messages to Kafka topic
write_to_kafka("tweet-test", x_test_df, y_test_df)