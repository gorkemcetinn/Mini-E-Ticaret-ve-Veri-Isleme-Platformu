from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from kafka import KafkaConsumer
from datetime import datetime
import json
import pandas as pd
import os

# Function to process sales for a given execution date
def process_sales(**context):
    ds = context['ds']  # execution date in 'YYYY-MM-DD'

    # Initialize Kafka consumer with timeout to end iteration
    consumer = KafkaConsumer(
        'sales_topic',
        bootstrap_servers='kafka:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=False,
        group_id=f'sales_group_{ds}',
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        consumer_timeout_ms=5000  # stop iteration after timeout
    )

    sales = []
    for msg in consumer:
        sale = msg.value
        ts = sale.get('timestamp', '')
        # match messages exactly for the execution date
        if ts.split('T')[0] == ds:
            sales.append(sale)
    consumer.close()

    if not sales:
        print(f"No sales data for {ds}")
        return

    # Create DataFrame and save CSV
    df = pd.DataFrame(sales)
    output_dir = os.path.join(os.getcwd(), 'data', 'sales')

    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f'daily_sales_{ds}.csv')

    df.to_csv(file_path, index=False)
    print(f"Saved {len(sales)} sales records to {file_path}")

# Define the DAG
default_args = {
    'owner': 'airflow',
    'retries': 1
}

dag = DAG(
    dag_id='process_sales_dag',
    default_args=default_args,
    description='Process daily sales data from Kafka',
    schedule_interval='30 12 * * *',  
    start_date=days_ago(1),
    catchup=False,
    tags=['ecommerce', 'sales']
)

# Task to process sales
process_task = PythonOperator(
    task_id='process_sales',
    python_callable=process_sales,
    provide_context=True,
    dag=dag
)
