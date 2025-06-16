from sqlalchemy import create_engine
import pandas as pd


DB_ENGINE=create_engine("postgresql+psycopg2://test-user:pass123@localhost/macro_datalake")


def extract_from_silver():
    t_name='silver_fred_cleaned'
    print(f'Extracting cleaned data: {t_name} table')
    cleaned_data=pd.read_sql(f"SELECT * from {t_name};",DB_ENGINE)
    return cleaned_data

def pivot_table(cleaned_data_silver):

    pivoted_data=cleaned_data_silver.pivot_table(
         columns='series_id',
         values='value',
         index='date',
         aggfunc='mean'
    )
    pivoted_data=pivoted_data.resample('D').ffill().bfill()
    
    pivoted_data.dropna(inplace=True)

    return pivoted_data
     

def load_gold_table(data):
    t_name='gold_macro_features'
    data.to_sql(
        t_name,
        con=DB_ENGINE,
        if_exists='replace',
    )
    print(f'Wide table is in {t_name} table and ready for ML!')

def gold_etl():
    cleaned_data_silver=extract_from_silver()
    wide_table=pivot_table(cleaned_data_silver)
    load_gold_table(wide_table)

if __name__=='__main__':
    gold_etl()