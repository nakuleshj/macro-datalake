
import pandas as pd
from prophet import Prophet
from sqlalchemy import create_engine
import os
from datetime import datetime,timedelta
from pandas.tseries.holiday import USFederalHolidayCalendar as holidays
from prophet.serialize import model_to_json

DB_ENGINE=create_engine("postgresql+psycopg2://test-user:pass123@localhost/macro_datalake")
MODEL_DIR = os.getenv("MODEL_DIR", "models/")
os.makedirs(MODEL_DIR, exist_ok=True)


def load_data():
    query = "SELECT * FROM gold_macro_features ORDER BY date;"
    df = pd.read_sql(query, DB_ENGINE)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date',inplace=True)
    return df

def train_model(SP500_data):
    split_date= datetime.today()- timedelta(weeks=13)
    split_date.date()
    SP500_train= SP500_data.loc[SP500_data.index <= split_date]

    SP500_train_prophet=SP500_train.reset_index()
    SP500_train_prophet.columns=['ds','y']
    SP500_train_prophet.head()
    hol=holidays()

    hds=hol.holidays(
    start=SP500_data.index.min(),
    end=SP500_data.index.max(),
    return_name=True
    )
    hds_df=pd.DataFrame(hds,columns=['holiday'])
    hds_df=hds_df.reset_index().rename(columns={'index':'ds'})
    
    forecast_model=Prophet(holidays=hds_df)
    forecast_model.fit(SP500_train_prophet)

    return forecast_model

def export_model(model):

    with open('./models/SP500_forecast_model.json','w') as fout:
        fout.write(model_to_json(model))

def te_model():
    gold_data=load_data()
    SP500_data=gold_data['SP500']
    SP500_model=train_model(SP500_data)
    export_model(SP500_model)

if __name__=='__main__':
    te_model()
