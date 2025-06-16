from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os, sys

SCRIPT_DIR = os.path.join(os.path.dirname(__file__), "scripts")
sys.path.append(SCRIPT_DIR)

import bronze_ingest
import silver_transform
import gold_aggregate


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 15, 16),
    'retries': 1,
}

with DAG(
    dag_id='macro_medallion_etl',
    default_args=default_args,
    schedule='@daily',
    catchup=False,
    tags=['macro', 'minio', 'medallion'],
) as dag:
    bronze_task = PythonOperator(
        task_id='bronze_layer',
        python_callable=bronze_ingest.bronze_el
    )