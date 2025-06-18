import requests, os, json
from datetime import date,timedelta,datetime
from dotenv import load_dotenv
from minio import Minio
from minio import S3Error
from airflow import DAG
from airflow.operators.python import PythonOperator


load_dotenv()


FRED_API_KEY=os.getenv('FRED_KEY')
FRED_ENDPOINT=os.getenv('FRED_ENDPOINT')

observation_start=date.today()-timedelta(weeks=10*52) #Last 20 years
observation_end=date.today()

def fetch_fred_data(series_id):
    params={
        'api_key':FRED_API_KEY,
        'file_type':'json',
        'series_id':series_id,
        'observation_start':observation_start
    }
    response=requests.get(
            FRED_ENDPOINT,
            params=params
        )
    response.raise_for_status()
    return response.json()
    
MINIO_CLIENT = Minio(
    endpoint='minio:9000',
    access_key='minioadmin',
    secret_key='admin123',
    secure=False,
)
BUCKET = 'bronze'


if not MINIO_CLIENT.bucket_exists(BUCKET):
    MINIO_CLIENT.make_bucket(BUCKET)

def upload_to_minio(series_id,data):
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f'{series_id}.json'
    object_path= f'{today}/{filename}'

    with open(filename,"w") as f:
        json.dump(data,f)
    
    try:
        MINIO_CLIENT.fput_object(
            bucket_name=BUCKET,
            object_name=object_path,
            file_path=filename,
            content_type='application/json'
        )
        print(f"Uploaded {object_path} to bucket '{BUCKET}'")
    except S3Error as e:
        print(f"Upload error: {e}")
    finally:
        os.remove(filename)


def load_to_bronze(series_list):
    for series_id in series_list:
        response=fetch_fred_data(series_id)
        if len(response)!=0:
            upload_to_minio(series_id=series_id,data=response)

def bronze_el():
    series_list=['SP500','UNRATE','CPIAUCSL','GDPC1','M2SL','FEDFUNDS','UMCSENT','DTWEXBGS','VIXCLS','PAYEMS','INDPRO']
    load_to_bronze(series_list)

if __name__=='__main__':
    bronze_el()    

with DAG(
    dag_id="bronze_ingest",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    task = PythonOperator(
        task_id="bronze_el",
        python_callable=bronze_el,
    )