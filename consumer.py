from kafka import KafkaConsumer
import json

if __name__ == "__main__":
    consumer = KafkaConsumer(
        'clickstream-topic',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='clickstream-group',
    )
    
    for message in consumer:
        event = message.value
        print(f"Received: {event}")
