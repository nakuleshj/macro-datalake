import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import os

DB_ENGINE=create_engine("postgresql+psycopg2://test-user:pass123@localhost/macro_datalake")


@st.cache_data(ttl=600)
def load_data():
    query = "SELECT * FROM gold_macro_features ORDER BY date;"
    df = pd.read_sql(query, DB_ENGINE)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date',inplace=True)
    return df

df = load_data()

st.sidebar.title("MacroLake Dashboard")
section = st.sidebar.radio("Navigate to", ["Trends", "View Data", "EDA"])

if section == "Trends":
    st.title("Indicator Time Series")
    series = st.selectbox("Select indicator", df.columns)
    show_30d_ma= st.checkbox("Add 30-day Moving Average")
    show_90d_ma= st.checkbox("Add 90-day Moving Average")
    fig = px.line(df, x=df.index, y=series, title=f"{series} Over Time")
    st.plotly_chart(fig, use_container_width=True)

if section == "View Data":
    st.title("Indicator Data")

    cols=st.multiselect("Select indicators:", df.columns,default=df.columns[0])
    st_date=st.date_input("Start date:", value=df.index[0], min_value=df.index[0], max_value=df.index[-1], key=None, help=None, on_change=None, args=None, kwargs=None, format="YYYY/MM/DD", disabled=False, label_visibility="visible")
    end_date=st.date_input("Start date:", value=df.index[-1], min_value=df.index[0], max_value=df.index[-1], key=None, help=None, on_change=None, args=None, kwargs=None, format="YYYY/MM/DD", disabled=False, label_visibility="visible")
    st.dataframe(df[st_date:][cols],use_container_width=True)
