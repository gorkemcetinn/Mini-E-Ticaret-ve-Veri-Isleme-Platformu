# app/Dockerfile
FROM python:3.10-slim

# Çalışma dizinini belirle
WORKDIR /app

# Gerekli dosyaları kopyala
COPY . .

# Bağımlılıkları yükle
RUN pip install --no-cache-dir flask kafka-python

# Uygulamayı başlat
CMD ["python", "app.py"]
