import requests, os, json
from datetime import date,timedelta
import psycopg2
from dotenv import load_dotenv

load_dotenv()

FRED_API_KEY=os.getenv('FRED_KEY')
FRED_ENDPOINT=os.getenv('FRED_ENDPOINT')

DB_USER=os.getenv('DB_USER')
DB_PWD=os.getenv('DB_PASS')
DB_NAME=os.getenv('DB_NAME')
DB_HOST=os.getenv('DB_HOST')
DB_PORT=os.getenv('DB_PORT')

print(DB_PWD)

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
            insert_query="""
            INSERT INTO bronze_fred_raw (series_id,response)
            VALUES (%s,%s)
            """
            response=fetch_fred_data(series_id)
            if len(response)!=0:
                cursor.execute(insert_query,(series_id,json.dumps(response)))
            cursor.close()
    except Exception as e:
        print(f"Error occured:{e}")    

load_to_sql('SP500')