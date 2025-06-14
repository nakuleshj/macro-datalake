from sqlalchemy import create_engine
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import shap, os, joblib
import numpy as np
import matplotlib.pyplot as plt

MODEL_DIR = "../models/"
os.makedirs(MODEL_DIR, exist_ok=True)

def get_gold_data():
    t_name='gold_macro_features'
    DB_ENGINE=create_engine("postgresql+psycopg2://test-user:pass123@localhost/macro_datalake")
    gold_data=pd.read_sql(f"SELECT * from {t_name};",DB_ENGINE)
    return gold_data

def train_model(gold_data):
    gold_data=gold_data.sort_values('date')
    print(gold_data.dtypes)
    gold_data["target"] = gold_data["DTWEXBGS"].shift(-1)
    gold_data.dropna(inplace=True)
    gold_data = gold_data.dropna(subset=["DTWEXBGS"])
    gold_data.set_index('date',inplace=True)
    X, y = gold_data.drop(['DTWEXBGS','target'], axis=1), gold_data[['target']]
    X = X.replace([np.inf, -np.inf], np.nan)

    valid_idx = X.dropna().index
    X = X.loc[valid_idx]
    y = y.loc[valid_idx]

    model = xgb.XGBRegressor(
        n_estimators=100,
        max_depth=3,
        learning_rate=0.1
    )

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
    model.fit(X_train, y_train)
    
    return model, X_train

def generate_shap(model, X_train):
    explainer = shap.Explainer(model)
    shap_values = explainer(X_train)

    plt.figure(figsize=(10, 6))
    shap.summary_plot(shap_values, X_train, show=False)
    plt.tight_layout()
    plt.savefig(os.path.join(MODEL_DIR, "shap_summary_plot.png"))
    plt.close()

def save_model(model):
    joblib.dump(model, os.path.join(MODEL_DIR,"dollar_xgb.model"))

def train_test_save_model():
    print('Loading data')
    gold_data=get_gold_data()
    print('Training model')
    model, X_train = train_model(gold_data)
    
    print('Generating SHAP plots')
    generate_shap(model, X_train)

    print('Saving model')
    save_model(model)

    print("All tasks completed!")

if __name__=="__main__":
    train_test_save_model()