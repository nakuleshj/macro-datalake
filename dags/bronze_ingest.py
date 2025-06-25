import json
import os
from datetime import date, datetime, timedelta

import requests
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from dotenv import load_dotenv
from minio import Minio, S3Error

# Load variables from .env file for use in this script
load_dotenv()

# Access FRED API key from .env file 
FRED_API_KEY = os.getenv("FRED_KEY")

# FRED API Endpoint to fetch observation values for a series
FRED_OBS_ENDPOINT = "https://api.stlouisfed.org/fred/series/observations"

# FRED API endpoint to fetch information on a series
FRED_SERIES_INFO = "https://api.stlouisfed.org/fred/series"

# Observation values for the last 10 years
observation_start = date.today() - timedelta(weeks=10 * 52)
observation_end = date.today()

# Fetch data for the specified series ID from a specified FRED API endpoint 
def fetch_fred_data(series_id: str, endpoint: str):
    params = {
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "series_id": series_id,
    }
    if endpoint == FRED_OBS_ENDPOINT:
        params["observation_start"] = observation_start
    response = requests.get(endpoint, params=params)
    response.raise_for_status()
    return response.json()

# Establish connection to the MinIO server
MINIO_CLIENT = Minio(
    endpoint="minio:9000",
    access_key="minioadmin",
    secret_key="admin123",
    secure=False,
)

# Define MinIO bucket for the bronze layer 
BUCKET = "bronze"

# Create a MinIO bucket if it does not currently exist
if not MINIO_CLIENT.bucket_exists(BUCKET):
    MINIO_CLIENT.make_bucket(BUCKET)


def upload_to_minio(series_id, data):
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"{series_id}.json"
    object_path = f"{today}/{filename}"

    with open(filename, "w") as f:
        json.dump(data, f)

    try:
        MINIO_CLIENT.fput_object(
            bucket_name=BUCKET,
            object_name=object_path,
            file_path=filename,
            content_type="application/json",
        )
        print(f"Uploaded {object_path} to bucket '{BUCKET}'")
    except S3Error as e:
        print(f"Upload error: {e}")
    finally:
        os.remove(filename)


def load_to_bronze(series_list):
    for series_id in series_list:
        
        response = fetch_fred_data(series_id, FRED_OBS_ENDPOINT)
        
        info = fetch_fred_data(series_id, FRED_SERIES_INFO)
        
        response["series_info"] = info["seriess"]
        
        if len(response) != 0:
            upload_to_minio(series_id=series_id, data=response)


def bronze_el():
    series_list = [
        "SP500",
        "UNRATE",
        "CPIAUCSL",
        "GDPC1",
        "M2SL",
        "FEDFUNDS",
        "UMCSENT",
        "DTWEXBGS",
        "VIXCLS",
        "PAYEMS",
        "INDPRO",
    ]
    load_to_bronze(series_list)


# DAG run daily
with DAG(
    dag_id="bronze_ingest",
    start_date=datetime(2024, 1, 1, 9),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    # Fetch from FRED API and load raw data to MinIO bronze bucket
    bronze_el_task = PythonOperator(
        task_id="bronze_el",
        python_callable=bronze_el,
    )
    # Trigger silver_transform DAG 
    trigger_silver = TriggerDagRunOperator(
        task_id="trigger_silver",
        trigger_dag_id="silver_transform",
    )
    bronze_el_task >> trigger_silver
