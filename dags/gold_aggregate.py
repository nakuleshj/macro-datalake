from datetime import datetime

import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from sqlalchemy import create_engine

DB_ENGINE = create_engine(
    "postgresql+psycopg2://test-user:pass123@macrolake-postgres:5432/macro_datalake"
)


def extract_from_silver():
    t_name = "silver_fred_cleaned"
    print(f"Extracting cleaned data: {t_name} table")
    cleaned_data = pd.read_sql(f"SELECT * from {t_name};", DB_ENGINE)
    return cleaned_data


def long_silver_to_wide_gold(cleaned_data_silver):

    pivoted_data = cleaned_data_silver.pivot_table(
        columns="series_id", values="value", index="date", aggfunc="mean"
    )
    pivoted_data = pivoted_data.resample("D").ffill().bfill()

    pivoted_data.dropna(inplace=True)

    return pivoted_data


def load_gold_table(data):
    t_name = "gold_wide"
    data.to_sql(
        t_name,
        con=DB_ENGINE,
        if_exists="replace",
    )
    print(f"Wide table is in {t_name} table and ready for ML!")


def gold_etl():
    cleaned_data_silver = extract_from_silver()
    wide_gold_table = long_silver_to_wide_gold(cleaned_data_silver)
    load_gold_table(wide_gold_table)


if __name__ == "__main__":
    gold_etl()

with DAG(
    dag_id="gold_aggregate",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:
    task = PythonOperator(
        task_id="gold_etl",
        python_callable=gold_etl,
    )
    task
