#!/usr/bin/env python3

# Packages import
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from kafka import KafkaProducer

# Bootstrap servers variable definition
BOOTSTRAP_SERVERS = [f"kafka{i+1}:{9092 + 2*i}" for i in range(int(sys.argv[1]))]

# Error management
def error_callback(exc):
    raise Exception(f"Error while sending data to kafka: {str(exc)}")
    
# Producer creation
def write_to_kafka(topic_name, messages, labels):
    count = 0
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
    for data in range(10000):
        producer.send(topic_name,
                    key=labels.iat[data].encode('utf-8'),
                    value=messages.iat[data, 0].encode('utf-8')).add_errback(error_callback)
                    
        count += 1
    producer.flush()
    print(f"Wrote {count} messages into topic: {topic_name}")

# Data loading
df = pd.read_csv(r"/pipeline/data/tweet_dataset.csv")

# Cleaning dataset
df = df[df['Language'] == 'en'].reset_index(drop=True)
df = df[['Text', 'Label']]

# Splitting in training and testing set
train_df, test_df = train_test_split(df, test_size=0.4, shuffle=True)

# Splitting into explanatory variables and response variable
x_train_df = train_df.drop(['Label'], axis=1)
y_train_df = train_df['Label']

# Saving testing set locally
test_df.to_parquet(r"/pipeline/data/test_df.parquet")

# Sending messages to Kafka topic
write_to_kafka("tweet-train", x_train_df, y_train_df)