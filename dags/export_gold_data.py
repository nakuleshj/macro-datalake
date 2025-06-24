from datetime import datetime

import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
import os
from sqlalchemy import create_engine

DB_ENGINE = create_engine(
    "postgresql+psycopg2://test-user:pass123@macrolake-postgres:5432/macro_datalake"
)

def get_gold_table(tname):
    print(f"Extracting gold table: {tname} table")
    gold_table = pd.read_sql(f"SELECT * from {tname};", DB_ENGINE)
    return gold_table

def export_to_csv(df: pd.DataFrame,filename):
    df.to_csv(f'{filename}.csv',index=False)

def export_gold_tables_to_csv():
    print(os.path.dirname(os.path.realpath(__file__)))
    macro_data=get_gold_table('fact_gold_wide')
    export_to_csv(macro_data,'fact_gold_wide')

    dim_series_info=get_gold_table('dim_series_info')
    export_to_csv(dim_series_info,'dim_series_info')
    print(os.listdir())

with DAG(
    dag_id="export_gold_data",
    start_date=datetime(2024, 1, 1, 9),
    schedule_interval=None,
    catchup=False,
) as dag:
    export_task = PythonOperator(
        task_id="export_csv",
        python_callable=export_gold_tables_to_csv,
    )

    export_task