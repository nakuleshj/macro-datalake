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
    pivoted_data=pivoted_data.resample('ME').mean()
    
    pivoted_data.dropna(inplace=True)
    pivoted_data['DTWEXBGS']=pivoted_data['DTWEXBGS'].astype(int)
    pct_change_df=pivoted_data.pct_change(periods=12)*1000
    pct_change_df.drop(columns='DTWEXBGS',inplace=True)

    #rolling_3ma_df=pivoted_data.rolling(window=3).mean()
    #rolling_3ma_df.drop(columns='DTWEXBGS',inplace=True)

    #rolling_6ma_df=pivoted_data.rolling(window=6).mean()
    #rolling_6ma_df.drop(columns='DTWEXBGS',inplace=True)
    
    merged_data=pivoted_data.merge(pct_change_df,how='left',on='date',suffixes=("","_yoy_growth"))
    #merged_data=merged_data.merge(rolling_3ma_df,how='left',on='date',suffixes=("","_3ma"))
    #merged_data=round(merged_data.merge(rolling_3ma_df,how='left',on='date',suffixes=("","_6ma")),2)
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