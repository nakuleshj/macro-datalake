from sqlalchemy import create_engine
import pandas as pd

def extract_from_silver():
    engine=create_engine("postgresql+psycopg2://test-user:pass123@localhost/macro-datalake")
    with engine.connect() as conn:
            cleaned_data=pd.read_sql("SELECT * from silver_fred_cleaned;",conn)
            return cleaned_data

def engineer_macro_features():
    cleaned_data=extract_from_silver()
    
    cleaned_data.set_index('date',inplace=True)
    cleaned_data['yoy_growth']=cleaned_data.groupby('series_id')['value'].pct_change(periods=12)*100
    cleaned_data['yoy_growth']=round(cleaned_data['yoy_growth'],2)
    select_USREC=cleaned_data['series_id']=='USREC'
    USREC_data=cleaned_data.loc[select_USREC,'value']
    cleaned_data['recession_flag']=USREC_data
    cleaned_data['recession_flag'].interpolate(inplace=True)

    

    print(cleaned_data.columns)
    
    print(cleaned_data.tail())


if __name__=='__main__':
    engineer_macro_features()