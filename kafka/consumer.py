#!/usr/bin/env python3
import json
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'sales_topic',
    bootstrap_servers='kafka:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='consumer-test-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("Dinleniyor: sales_topic")
for msg in consumer:
    print(f"Received: {msg.value}")
