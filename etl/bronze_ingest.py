import requests, os, json
from datetime import date,timedelta
import psycopg2
from dotenv import load_dotenv

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
        'observation_start':observation_start,
        'observation_end':observation_end
    }
    try:
        response=requests.get(
            FRED_ENDPOINT,
            params=params
        )
        return response.json()
    except Exception as e:
        print(f'Error: {e}')
        return {}

def load_to_sql(series_id):
    db_params={
        'dbname': 'macro-datalake',
        'user': 'test-user',
        'password':'pass123',
        'host': 'localhost',
        'port': 5432
    }
    try:
        with psycopg2.connect(**db_params) as conn:
            cursor=conn.cursor()
            
            cursor.execute('TRUNCATE bronze_fred_raw')

            insert_query="""
            INSERT INTO bronze_fred_raw (series_id,response)
            VALUES (%s,%s)
            """
            
            for series_id in series_list:
                response=fetch_fred_data(series_id)
                if len(response)!=0:
                    cursor.execute(insert_query,(series_id,json.dumps(response)))
                    conn.commit()
            cursor.close()

    except Exception as e:
        print(f"Error occured:{e}")    

if __name__=='__main__':
        series_list=['SP500','USREC','UNRATE','CPIAUCSL','PAYEMS','GDPC1','M2SL','INDPRO','FEDFUNDS','T10Y2Y','HOUST','UMCSENT','BAA10Y']
        load_to_sql(series_list)