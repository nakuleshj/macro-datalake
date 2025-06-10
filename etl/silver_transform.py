import pandas as pd
import datetime as dt
from sqlalchemy import create_engine
from numpy import nan

def extract_from_bronze():
    engine=create_engine("postgresql+psycopg2://test-user:pass123@localhost/macro-datalake")
    with engine.connect() as conn:
            raw_data=pd.read_sql("SELECT * from bronze_fred_raw;",conn)
            return raw_data

def load_to_silver(transformed_data: pd.DataFrame):
    try:
        engine=create_engine("postgresql+psycopg2://test-user:pass123@localhost/macro-datalake")
        with engine.connect() as conn:
            transformed_data.to_sql('silver_fred_cleaned',conn,if_exists='replace')

    except Exception as e:
        print(f"Error occured:{e}")   

def transform(raw_data):
    transformed_data=pd.DataFrame()
    row_cnt=0
    for i, row in raw_data.iterrows():
        obs=pd.DataFrame(row['response']['observations'])
        
        obs.drop(['realtime_end','realtime_start'],axis=1,inplace=True)
          
        obs['series_id']=row['series_id']

        obs['date']=pd.to_datetime(obs['date'])

        obs['frequency']=pd.infer_freq(obs['date'])

        obs.loc[obs['value']==".",'value']=nan          
        obs['value']=obs['value'].astype(float).round(2)
        obs['value']=obs['value'].interpolate()

        transformed_data=pd.concat([transformed_data,obs],axis=0)
        
        return transformed_data

if __name__=="__main__":
    raw_data=extract_from_bronze()
    transformed_data=transform(raw_data)
    load_to_silver(transformed_data)