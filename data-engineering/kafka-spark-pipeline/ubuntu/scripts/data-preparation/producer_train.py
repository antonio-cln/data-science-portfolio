#!/usr/bin/env python3

import sys
import time

import pandas as pd
from sklearn.model_selection import train_test_split

from kafka import KafkaProducer
from kafka.errors import KafkaError

BOOTSTRAP_SERVERS = [f"127.0.0.1:{9092 + 2*i}" for i in range(int(sys.argv[1]))]

def error_callback(exc):
    raise Exception(f"Error while sending data to kafka: {str(exc)}")
    
def write_to_kafka(topic_name, messages, labels):
    count = 0
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
    for data in range(150000):
        producer.send(topic_name,
                    key=labels.iat[data].encode('utf-8'),
                    value=messages.iat[data, 0].encode('utf-8')).add_errback(error_callback)
                    
        count += 1
    producer.flush()
    print(f"Wrote {count} messages into topic: {topic_name}")

df = pd.read_csv("dataset.csv")

df = df[df['Language'] == 'en'].reset_index(drop=True)
df = df[['Text', 'Label']]

train_df, test_df = train_test_split(df, test_size=0.4, shuffle=True)

x_train_df = train_df.drop(['Label'], axis=1)
y_train_df = train_df['Label']

test_df.to_parquet("test_df.parquet")

start_time = time.time()
write_to_kafka("tweet-train", x_train_df, y_train_df)
end_time = time.time()
print(f"Time elapsed: {end_time-start_time}")
