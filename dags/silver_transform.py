import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine,text
from numpy import nan
from minio import Minio, S3Error
import json
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

def extract_from_bronze():
    today = datetime.now().strftime("%Y-%m-%d")
    minio_client=Minio(
        endpoint='minio:9000',
        access_key='minioadmin',
        secret_key='admin123',
        secure=False,
    )
    bucket_name='bronze'
    objects = minio_client.list_objects(bucket_name, recursive=True)

    raw_data=[]

    for obj in objects:
        print(f'Reading object:{obj.object_name}')
        response = minio_client.get_object(bucket_name, obj.object_name)
        json_data = json.loads(response.read().decode("utf-8"))
        json_data['series_id']=obj.object_name.split('/')[1].split('.')[0]
        raw_data.append(json_data)
    raw_data_df=pd.DataFrame(raw_data)
    return raw_data_df
        

def load_to_silver(transformed_data: pd.DataFrame):
    try:
        engine=create_engine("postgresql+psycopg2://test-user:pass123@macrolake-postgres:5432/macro_datalake")
        with engine.connect() as conn:
            transformed_data.to_sql('silver_fred_cleaned',conn,if_exists='replace',index=False)

    except Exception as e:
        print(f"Error occured:{e}")  

def transform(raw_data: pd.DataFrame):
    transformed_data=pd.DataFrame()

    for i, row in raw_data.iterrows():
        obs=pd.DataFrame(row['observations'])
        
        obs.drop(['realtime_end','realtime_start'],axis=1,inplace=True)
          
        obs['series_id']=row['series_id']

        obs['date']=pd.to_datetime(obs['date'])

        obs['frequency']=pd.infer_freq(obs['date'])

        obs.loc[obs['value']==".",'value']=nan          
        obs['value']=obs['value'].astype(float).round(2)
        obs['value']=obs['value'].interpolate()

        transformed_data=pd.concat([transformed_data,obs],axis=0)
        
    return transformed_data

def silver_etl():
    raw_data=extract_from_bronze()
    transformed_data=transform(raw_data)
    load_to_silver(transformed_data)

if __name__=="__main__":
    silver_etl()

with DAG(
    dag_id="silver_transform",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:
    task = PythonOperator(
        task_id="silver_etl",
        python_callable=silver_etl,
    )
    trigger_gold=TriggerDagRunOperator(
            task_id='trigger_gold',
            trigger_dag_id='gold_aggregate',
        )
    task >> trigger_gold