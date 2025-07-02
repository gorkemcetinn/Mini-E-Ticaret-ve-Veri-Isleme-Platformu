from flask import Flask, render_template, redirect
from kafka import KafkaProducer
import json
from datetime import datetime

app = Flask(__name__)

# Kafka producer; Docker Compose içindeki servise 'kafka:9092' üzerinden bağlanıyoruz
producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Örnek ürün listesi
products = [
    {"id": 1, "name": "Kitap",   "price": 50},
    {"id": 2, "name": "Mouse",   "price": 100},
    {"id": 3, "name": "Klavye",  "price": 150}
]

@app.route('/')
def index():
    return render_template('index.html', products=products)

@app.route('/buy/<int:product_id>')
def buy(product_id):
    # Ürünü bul ve event oluştur
    product = next(p for p in products if p["id"] == product_id)
    event = {
        "product_id": product["id"],
        "name": product["name"],
        "price": product["price"],
        "timestamp": datetime.utcnow().isoformat()
    }
    # Kafka topic'ine gönder
    producer.send('sales_topic', event)
    producer.flush()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
