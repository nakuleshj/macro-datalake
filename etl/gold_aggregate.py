from sqlalchemy import create_engine
import pandas as pd

def extract_from_silver():
    engine=create_engine("postgresql+psycopg2://test-user:pass123@localhost/macro-datalake")
    with engine.connect() as conn:
            cleaned_data=pd.read_sql("SELECT * from silver_fred_cleaned;",conn)
            return cleaned_data

def engineer_macro_features():

    pivoted_data=extract_from_silver().pivot(
         columns='series_id',
         values='value',
         index='date'
    )

    pivoted_data=pivoted_data.ffill().bfill()
    pivoted_data=pivoted_data.resample('ME').mean()
    print(round(pivoted_data.pct_change()*1000,2).drop(columns='USREC'))


if __name__=='__main__':
    engineer_macro_features()