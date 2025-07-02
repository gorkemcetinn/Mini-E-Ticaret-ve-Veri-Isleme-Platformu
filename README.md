
# 💼 Mini E-Ticaret + Kafka + Airflow Projesi

Bu proje, küçük bir e-ticaret web uygulaması üzerinden yapılan satışları Kafka ile mesaj kuyruğuna gönderir ve Airflow ile her gün saat **15:30**'da bu satışları CSV formatında işler.

## 🔧 Proje Bileşenleri

### 1. `app/` – Flask Web Uygulaması

- Basit bir ürün listesi görüntülenir.
- "Satın Al" butonuna tıklandığında Kafka'ya satış mesajı gönderilir.
- Flask uygulaması port **5000**'de çalışır.

### 2. `airflow/` – Apache Airflow

- `dags/process_sales_dag.py`: Kafka’dan verileri okuyup `/opt/airflow/data/sales` dizinine CSV olarak yazan DAG.
- Bu DAG her gün **15:30 yerel saat**'te tetiklenir.

### 3. `kafka/` – Apache Kafka & Zookeeper

- `sales_topic` adında bir topic vardır.
- Flask uygulaması satışları buraya üretir.
- Airflow, bu topic'ten satış verilerini tüketir.

## 📦 Docker Servisleri (`docker-compose.yml`)

| Servis              | Açıklama                                                         |
|---------------------|------------------------------------------------------------------|
| `web`               | Flask uygulamasını barındırır.                                   |
| `zookeeper`         | Kafka için gerekli servis.                                       |
| `kafka`             | Kafka broker.                                                    |
| `kafka-ui`          | Kafka topiclerini ve mesajları görüntülemek için web arayüzü.    |
| `postgres`          | Airflow için metadata veritabanı.                                |
| `redis`             | Celery için mesaj kuyruğu.                                       |
| `airflow-init`      | Airflow veritabanını başlatır ve admin kullanıcı oluşturur.      |
| `airflow-webserver` | Airflow arayüzü.                                                 |
| `airflow-scheduler` | DAG’leri tetikleyen servis.                                      |
| `airflow-worker`    | Airflow görevlerini çalıştırır.                                  |

## 📁 Proje Klasör Yapısı

```
E-TİCARET/

├── airflow/                  # Airflow için Dockerfile veya config dosyaları
│   └── Dockerfile            # Airflow image'ını özelleştirmek için kullanılır
│
├── app/                      # Flask web uygulaması
│   ├── templates/            # HTML şablonları
│   │   └── index.html        # Ürün listeleme ve satın alma sayfası
│   ├── app.py                # Flask uygulamasının giriş noktası
│   └── Dockerfile            # Flask uygulamasını container içinde çalıştırmak için Dockerfile
│
├── dags/                     # Airflow DAG dosyaları
│   └── process_sales_dag.py  # Günlük satış verilerini Kafka'dan okuyup CSV'ye yazan DAG
│
├── data/                     # Uygulamanın işlediği verilerin bulunduğu klasör
│   └── sales/                # Günlük satış verilerinin CSV dosyaları buraya yazılır
│
├── kafka/                    # Kafka producer/consumer scriptleri
│   ├── producer.py           # Ürün satın alındığında Kafka’ya mesaj yollayan script
│   └── consumer.py           # Kafka’dan veri okumak için kullanılabilir
│
├── logs/                     # Airflow log dosyaları
│
├── plugins/                  # (Opsiyonel) Airflow özel plugin’leri için klasör
│
├── docker-compose.yaml       # Tüm servisleri tanımlayan Docker Compose konfigürasyonu

```

## 🕒 Zamanlama

- Airflow DAG’i yerel saatle **15:30**'da çalışacak şekilde ayarlanmıştır.
- UTC+3

## 🛠️ Kurulum ve Çalıştırma

1. Proje dizinine gidin:
   ```bash
   cd -projedizini-
   ```

2. Gerekli Docker imajlarını oluşturun:
   ```bash
   docker-compose build
   ```

3. Servisleri başlatın:
   ```bash
   docker-compose up -d
   ```

4. Uygulamalara erişin:

   - Flask: [http://localhost:5000](http://localhost:5000)  
   - Kafka UI: [http://localhost:8080](http://localhost:8080)  
   - Airflow UI: [http://localhost:8081](http://localhost:8081)
  
5. 🔐 Airflow FERNET_KEY Nedir?
Airflow, bağlantı bilgileri gibi hassas verileri veri tabanında şifreleyerek saklar. Bu işlemi yapabilmek için FERNET şifreleme anahtarına ihtiyaç duyar.

Yani, FERNET_KEY, Airflow'un güvenlik için kullandığı şifreleme/deşifreleme anahtarıdır.

🔑 Nasıl Oluşturulur?
Yeni bir FERNET_KEY üretmek için aşağıdaki Python komutunu terminalde çalıştırabilirsiniz:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```
Elde edilen bu anahtar, docker-compose.yml dosyasındaki tüm Airflow servislerinin environment kısmına şu şekilde yazılmalıdır:

```bash
AIRFLOW__CORE__FERNET_KEY: '***'
```
❗ Not: FERNET anahtarı tüm servislerde aynı olmalıdır (webserver, scheduler, worker), aksi halde Airflow şifrelenmiş verileri okuyamaz ve hata alırsınız.

## 📄 CSV Dosyasına Erişim

CSV dosyası Airflow worker konteynerinde `/opt/airflow/data/sales` klasörüne kaydedilir. Dosyayı host makinenize almak için:

```bash
docker cp airflow_worker:/opt/airflow/data/sales/daily_sales_YYYY-MM-DD.csv ./data/sales/
```

> **Not:** Eğer `./data/sales` klasörünüzde CSV görünmüyorsa, `airflow-worker` servisine şu volume'ü eklediğinizden emin olun:

```yaml
volumes:
  - ./data/sales:/opt/airflow/data/sales
```

Bu değişiklik sonrası sistemi şu şekilde yeniden başlatabilirsiniz:

```bash
docker-compose down -v
docker-compose up --build -d
```
## 📸 Proje Görselleri


![web](https://github.com/user-attachments/assets/b79f853d-e5c4-4faa-92c7-c85f064ad3b2)
![realairflow](https://github.com/user-attachments/assets/e957c14e-5cb2-4345-ac95-e86e3ba068e7)
![kafka](https://github.com/user-attachments/assets/4f4d6a89-2636-4429-8a4e-a8496b67e17a)

