# airflow/Dockerfile
FROM apache/airflow:2.9.0

# Switch to airflow user to install additional Python packages
USER airflow
RUN pip install kafka-python pandas

# Switch back to default user
USER airflow
