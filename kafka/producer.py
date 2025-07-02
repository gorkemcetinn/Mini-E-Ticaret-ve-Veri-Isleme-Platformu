#!/usr/bin/env python3
import json
import random
import time
from datetime import datetime
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

products = [
    {"id": 1, "name": "Kitap",  "price": 50},
    {"id": 2, "name": "Mouse",  "price": 100},
    {"id": 3, "name": "Klavye", "price": 150},
    {"id": 4, "name": "Kalem",  "price": 10},
    {"id": 5, "name": "Defter", "price": 20}
]

if __name__ == "__main__":
    print("Başlatılıyor: sales_topic'e rastgele satış gönderimi")
    try:
        while True:
            p = random.choice(products)
            sale_event = {
                "product_id": p["id"],
                "name": p["name"],
                "price": p["price"],
                "amount": random.randint(1, 5),
                "timestamp": datetime.utcnow().isoformat()
            }
            producer.send('sales_topic', sale_event)
            producer.flush()
            print(f"Sent: {sale_event}")
            time.sleep(2)  # 2 saniyede bir yeni event
    except KeyboardInterrupt:
        print("Simülatör durduruldu.")
        producer.close()
