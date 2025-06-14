from sqlalchemy import create_engine
import pandas as pd


DB_ENGINE=create_engine("postgresql+psycopg2://test-user:pass123@localhost/macro_datalake")


def extract_from_silver():
    t_name='silver_fred_cleaned'
    print(f'Extracting cleaned data: {t_name} table')
    cleaned_data=pd.read_sql(f"SELECT * from {t_name};",DB_ENGINE)
    return cleaned_data

def engineer_macro_features(cleaned_data_silver):

    pivoted_data=cleaned_data_silver.pivot_table(
         columns='series_id',
         values='value',
         index='date',
         aggfunc='mean'
    )
    pivoted_data=pivoted_data.resample('D').ffill().bfill()
    
    pivoted_data.dropna(inplace=True)

    pct_change_df=pivoted_data.pct_change(periods=1)*100

    rolling_90d_df=pivoted_data.rolling(window=90).mean()
    rolling_90d_df.drop(columns='DTWEXBGS',inplace=True)

    rolling_180d_df=pivoted_data.rolling(window=180).mean()
    rolling_180d_df.drop(columns='DTWEXBGS',inplace=True)
    
    merged_data=pivoted_data.merge(pct_change_df,how='left',on='date',suffixes=("","_growth"))
    merged_data=merged_data.merge(rolling_90d_df,how='left',on='date',suffixes=("","_3ma"))
    merged_data=round(merged_data.merge(rolling_180d_df,how='left',on='date',suffixes=("","_6ma")),2)
    return merged_data
     

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
    wide_table=engineer_macro_features(cleaned_data_silver)
    load_gold_table(wide_table)

if __name__=='__main__':
    gold_etl()