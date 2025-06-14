import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import os

DB_ENGINE=create_engine("postgresql+psycopg2://test-user:pass123@localhost/macro_datalake")

st.set_page_config(layout="wide")

@st.cache_data(ttl=600)
def load_data():
    query = "SELECT * FROM gold_macro_features ORDER BY date;"
    df = pd.read_sql(query, DB_ENGINE)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date',inplace=True)
    return df

df = load_data()

st.title("MacroLake Exploratory Data Analysis (EDA)")

st.subheader("Snapshot of Data:")
st.dataframe(df.head(10),use_container_width=True)

st.subheader("Data Summary")
st.write(f"Total rows: {len(df)}")
st.write(f"Unique indicators: {df.columns.nunique()}")
st.write(f"Date range: {df.index.min().date()} → {df.index.max().date()}")

st.subheader("Trend")
dist_series = st.selectbox("Select indicator for histogram", df.columns)
dist_data = df[dist_series]
fig_hist = px.line(dist_data, x=df.index, y=dist_data )
st.plotly_chart(fig_hist, use_container_width=True)

st.subheader("Value Distribution")

fig_hist = px.histogram(dist_data, x=dist_data, nbins=30, title=f"{dist_series} Distribution")
st.plotly_chart(fig_hist, use_container_width=True)


st.subheader("Boxplot for Outlier Detection")
fig_box = px.box(dist_data, y=dist_data, title=f"{dist_series} Boxplot")
st.plotly_chart(fig_box, use_container_width=True)


st.subheader("Correlation Heatmap")

corr_cols=st.multiselect("Select Indicators:",options=df.columns,default=df.columns[0:2])

corr=df[corr_cols].corr().round(2)
fig=px.imshow(corr, text_auto=True, color_continuous_scale='rdylgn', title="Correlation Matrix")

st.plotly_chart(fig)
