import pandas as pd
import psycopg2
import datetime as dt
from sqlalchemy import create_engine
from numpy import nan
import json, time

def extract_from_bronze():
    db_params={
        'dbname': 'macro-datalake',
        'user': 'test-user',
        'password':'pass123',
        'host': 'localhost',
        'port': 5432
    }
    engine=create_engine("postgresql+psycopg2://test-user:pass123@localhost/macro-datalake")
    with engine.connect() as conn:
            raw_data=pd.read_sql("SELECT * from bronze_fred_raw;",conn)
            return raw_data

def convert(series):
     for s in series:
          print(s)
          print(float(s))

def transform(raw_data):
    transformed_data=pd.DataFrame()
    row_cnt=0
    for i, row in raw_data.iterrows():
        response=row['response']
        obs=pd.DataFrame(response['observations'])
        obs.drop(['realtime_end','realtime_start'],axis=1,inplace=True)
          
        obs['series_id']=row['series_id']
          
        obs['date']=pd.to_datetime(obs['date'])

        obs['frequency']=pd.infer_freq(obs['date'])

        obs.loc[obs['value']==".",'value']=nan          
        obs['value']=obs['value'].astype(float)
        obs['value']=obs['value'].interpolate()
        
        row_cnt+=obs.shape[0]
        transformed_data=pd.concat([transformed_data,obs],axis=0)
        
    if transformed_data.shape[0] == row_cnt:
         return transformed_data

if __name__=="__main__":
    raw_data=extract_from_bronze()
    transformed_data=transform(raw_data)
    print(transformed_data.head())