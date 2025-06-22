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
    info_cols = [
        "series_id",
        "title",
        "last_updated",
        "units",
        "units_short",
        "frequency",
    ]
    pivoted_data = cleaned_data_silver.drop(columns=info_cols[1:]).pivot_table(
        columns="series_id", values="value", index="date", aggfunc="mean"
    )

    pivoted_data = pivoted_data.resample("D").ffill().bfill()

    #pivoted_data.dropna(inplace=True)

    series_data = cleaned_data_silver[info_cols]
    series_data.drop_duplicates(subset=info_cols, keep="first", inplace=True)
    return pivoted_data, series_data


def load_gold_table(macro_data, series_data):
    macro_data.to_sql(
        "fact_gold_wide",
        con=DB_ENGINE,
        if_exists="replace",
    )
    print(f"Wide table is in the database and ready for ML!")
    series_data.to_sql(
        "dim_series_info", con=DB_ENGINE, if_exists="replace", index=False
    )


def gold_etl():
    cleaned_data_silver = extract_from_silver()
    wide_gold_table, series_data = long_silver_to_wide_gold(cleaned_data_silver)
    load_gold_table(wide_gold_table, series_data)


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
