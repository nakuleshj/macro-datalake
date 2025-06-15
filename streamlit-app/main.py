import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import os
from prophet.serialize import model_from_json

DB_ENGINE=create_engine("postgresql+psycopg2://test-user:pass123@localhost/macro_datalake")

st.set_page_config(layout="wide",page_title='MacroLake Dashboard')

@st.cache_data(ttl=600)
def load_data():
    query = "SELECT * FROM gold_macro_features ORDER BY date;"
    df = pd.read_sql(query, DB_ENGINE)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date',inplace=True)
    return df

df = load_data()

st.title("MacroLake ")
tab1, tab2, tab3 = st.tabs(["Exploratory Data Analysis (EDA)","Time Series Analysis: SP500", "Prophet-Based S&P 500 Prediction"])

with tab1:
    st.subheader("Snapshot of Data:")
    st.dataframe(df.head(10),use_container_width=True)

    st.write(f"Total rows: {df.shape[0]}")
    st.write(f"Unique indicators: {df.columns.nunique()}")
    st.write(f"Date range: {df.index.min().date()} → {df.index.max().date()}")

    
    st.subheader("Key Statistics")
    st.dataframe(df.describe().round(2))
    
    
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

with tab2:
    print('')

with tab3:
    fcst_period=st.number_input('Enter forecast period (months)',min_value=1,value=3,max_value=12)
    fin= open('../ml/models/SP500_forecast_model.json', 'r')
    m = model_from_json(fin.read())     
    fcst_df=m.make_future_dataframe(periods=fcst_period*30,freq='D',include_history=False)    
    fcsts=m.predict(fcst_df)
    plot_df=pd.concat([df['SP500'],fcsts.set_index('ds')['yhat']],axis=1)
    plot_df.columns=['Actual','Forecasted']
    st.dataframe(plot_df)

    st.line_chart(plot_df,color=['#000000','#ff0000'])