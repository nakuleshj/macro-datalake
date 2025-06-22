import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from prophet import Prophet
from prophet.plot import plot_components_plotly
import plotly.graph_objects as go
from sklearn.metrics import mean_absolute_percentage_error
from pandas.tseries.holiday import USFederalHolidayCalendar as holidays


DB_ENGINE = create_engine(
    "postgresql+psycopg2://test-user:pass123@macrolake-postgres:5432/macro_datalake"
)
DB_ENGINE_AIRFLOW = create_engine(
    "postgresql://airflow:airflow@airflow-postgres:5432/airflow"
)

st.set_page_config(layout="wide", page_title="MacroLake Dashboard")


@st.cache_data(ttl=600)
def load_gold_data():
    with st.spinner("Loading economic data..."):
        query = "SELECT * FROM gold_wide ORDER BY date;"
        df = pd.read_sql(query, DB_ENGINE)
        df["date"] = pd.to_datetime(df["date"])
        df.set_index("date", inplace=True)
    return df


@st.cache_data(ttl=600)
def load_series_meta():
    with st.spinner("Loading economic data..."):
        query = "SELECT * FROM series_data;"
        df = pd.read_sql(query, DB_ENGINE)
    return df


def train_model(SP500_data):
    split_date = datetime.today() - timedelta(weeks=13)
    split_date.date()
    SP500_train = SP500_data.loc[SP500_data.index <= split_date]

    SP500_train_prophet = SP500_train.reset_index()
    SP500_train_prophet.columns = ["ds", "y"]
    SP500_train_prophet.head()
    hol = holidays()

    hds = hol.holidays(
        start=SP500_data.index.min(), end=SP500_data.index.max(), return_name=True
    )
    hds_df = pd.DataFrame(hds, columns=["holiday"])
    hds_df = hds_df.reset_index().rename(columns={"index": "ds"})

    forecast_model = Prophet(holidays=hds_df)
    forecast_model.fit(SP500_train_prophet)

    return forecast_model


def kpi_card(metric_name, current_value, delta_pct, unit="%", color="normal"):
    if color == "positive":
        delta_color = "green"
    elif color == "negative":
        delta_color = "red"
    else:
        delta_color = "gray"

    st.metric(
        label=metric_name,
        value=f"{current_value:.2f}{unit}",
        delta=f"{delta_pct:+.2f}{unit}",
        delta_color=delta_color,
    )


df = load_gold_data()

st.title("MacroLake Dashboard")

tab1, tab2, tab3 = st.tabs(
    [
        "Summary",
        "Indicators",
        "S&P 500 Forecasting with Prophet",
    ]
)
with tab1:
    st.subheader("Key Indicators")
    df_sorted = df.sort_index()
    ncol = len(df.columns)
    cols = st.columns(4)
    series_info = load_series_meta()
    for i in range(ncol):
        col = cols[i % 3]
        metric = df.columns[i]
        freq = series_info.loc[series_info["series_id"] == df.columns[i], "frequency"]
        latest_value = df[df.columns[i]].asfreq(freq.values[0])[-1]
        prev_value = df[df.columns[i]].asfreq(freq.values[0])[-2]
        unit = ""
        delta_pct = round((latest_value / prev_value - 1) * 100, 1)
        col.metric(metric, value=f"{latest_value:,.1f}{unit}", delta=f"{delta_pct}%")

    def plot_sparkline(df, title, yaxis_title):
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df.values,
                mode="lines",
                name=title,
                line=dict(color="royalblue"),
            )
        )
        fig.update_layout(
            height=300,
            title=title,
            xaxis_title="Date",
            yaxis_title=yaxis_title,
            margin=dict(l=20, r=20, t=40, b=20),
            template="plotly_white",
        )
        return fig

    with cols[3]:
        ind_tab1 = st.selectbox("Select an indicator to plot:", options=df.columns)
        st.plotly_chart(
            plot_sparkline(df[ind_tab1], "Real GDP (Billions $)", "Billions"),
            use_container_width=True,
        )
    st.caption("Data Source: FRED API (Federal Reserve Bank of St. Louis)")

with tab2:
    st.header("Economic Indicators Explorer")
    st.write("Explore time series of key macroeconomic indicators using official FRED data.")
    ind_tab2 = st.selectbox("Select an Indicator", df.columns)
    start_date = st.date_input("Start Date", datetime(2015, 1, 1))

    st.subheader("Latest Statistics")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Latest Value", f"{50:.2f}")
    with col2:
        #mom = latest['value'] - prev_month['value']
        st.metric("MoM Change", f"{5:+.2f}")
    with col3:
        if not False:
            #yoy = latest['value'] - prev_year['value'].values[0]
            st.metric("YoY Change", f"{10:+.2f}%")
        else:
            st.metric("YoY Change", "N/A")

    st.caption("Data Source: FRED (Federal Reserve Economic Data)")




with tab3:
    st.header("Forecasting the S&P 500 with Meta’s Prophet")
    
    st.markdown(
        """
    [Prophet](https://facebook.github.io/prophet/) is an open-source forecasting tool developed by Meta (formerly Facebook) for modeling **time series data with strong seasonality and trend components**. 

    It’s designed to handle real-world challenges such as:
    - Irregular or missing observations  
    - Multiple seasonal effects (weekly, yearly)  
    - Holiday impacts  
    - Sudden trend shifts (changepoints)  

    Prophet’s **additive time series model** makes it ideal for financial data like the S&P 500, where **transparency**, **interpretability**, and **flexibility** are key.

    ---

    ### Project Goal

    This module forecasts the **S&P 500 index** over **short- to medium-term horizons** (30 to 365 days) using Prophet, with the goal of providing:

    - **Investment timing and portfolio positioning**
    - **Market risk monitoring**
    - **Insight into seasonal and structural market patterns**

    The dashboard allows for custom tuning and exploration of assumptions to simulate different market scenarios — making it a useful tool for both **analytical insight** and **strategic decision support**.
    """
    )

    st.subheader("Forecasted S&P 500 vs Historical Data")

    fcst_period = st.slider(
        "Forecast Horizon (Days)",
        min_value=30,
        max_value=360,
        step=30,
        value=90,
        help="Select how far into the future you want to forecast the S&P 500 index.",
    )

    m = train_model(df["SP500"])
    fcst_df = m.make_future_dataframe(
        periods=fcst_period, freq="D", include_history=False
    )

    forecast = m.predict(fcst_df)

    split_date = df["SP500"].index.max() - timedelta(days=fcst_period)
    test_data = (
        df.loc[df.index > split_date, "SP500"]
        .reset_index()
        .rename(columns={"date": "ds"})
        .drop(columns="SP500")
    )

    test_df = m.predict(test_data)

    mape = (
        mean_absolute_percentage_error(
            df.loc[df.index > split_date, "SP500"], test_df["yhat"]
        )
        * 100
    )
    accuracy = round(100 - mape, 2)

    merged_df = pd.merge(
        df["SP500"].reset_index().rename(columns={"SP500": "Actual", "date": "ds"}),
        forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]],
        how="outer",
    )

    current_value = merged_df["Actual"].max()
    future_value = merged_df.loc[merged_df["ds"] == merged_df["ds"].max(), "yhat"]
    projected_change = ((future_value.values[0] - current_value) / current_value) * 100
    trend_icon = "🔺" if projected_change > 0 else "🔻"
    trend_color = "green" if projected_change > 0 else "red"

    col1, col2, col3 = st.columns(3)
    col1.metric("📊 Current S&P 500", f"{current_value:,.2f}")
    col2.metric(
        f"{trend_icon} {fcst_period}-Day Projected Change",
        f"{projected_change:.2f}%",
        delta_color="normal" if projected_change == 0 else "inverse",
    )
    col3.metric("🎯 Forecast Accuracy", f"{accuracy}%")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=merged_df["ds"],
            y=merged_df["Actual"],
            mode="lines",
            name="Actual",
            line=dict(color="blue"),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=merged_df["ds"],
            y=merged_df["yhat"],
            mode="lines",
            name="Forecast",
            line=dict(color="green", dash="dash"),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=pd.concat([merged_df["ds"], merged_df["ds"][::-1]]),
            y=pd.concat([merged_df["yhat_upper"], merged_df["yhat_lower"][::-1]]),
            fill="toself",
            fillcolor="rgba(0,255,0,0.2)",
            line=dict(color="rgba(255,255,255,0)"),
            hoverinfo="skip",
            showlegend=True,
            name="Confidence Interval",
        )
    )

    fig.update_layout(
        title="S&P 500 Forecast with Prophet",
        xaxis_title="Date",
        yaxis_title="Index Value",
        hovermode="x unified",
        template="plotly_white",
    )

    st.plotly_chart(fig, use_container_width=True)

    csv = forecast.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Export Forecast CSV",
        data=csv,
        file_name="sp500_forecast.csv",
        mime="text/csv",
    )

    st.subheader("Forecast Components")

    st.markdown(
        """
        The plots below show the internal decomposition of the time series forecast:

        - **Trend**: Long-term direction of the S&P 500
        - **Weekly Seasonality**: Recurring weekly patterns (e.g., Monday effect)
        - **Yearly Seasonality**: Annual market cycles or calendar effects
        - **Holidays**: Impact of market holidays (if included)
        """
    )

    with st.spinner("Generating component plots..."):
        components_fig = plot_components_plotly(m, forecast)
        st.plotly_chart(components_fig, use_container_width=True)

    st.subheader("Takeaways")

    st.markdown(
        f"""
    **According to the current model**, the S&P 500 is expected to continue {"an **upward**" if projected_change>0 else "a **downward**"} trend over the next **{fcst_period}** days, with forecasted values showing a **{projected_change:.2f}%** change from today.

    This forecast can support:
    - **Investment Timing**: Identifying entry/exit opportunities for institutional or retail investors  
    - **Risk Signals**: Monitoring deviations from trend that could indicate volatility or macroeconomic shifts  
    - **Strategic Planning**: Supporting treasury, allocation, or corporate strategy teams with expected market trajectories  
    - **Macro Sentiment Insight**: Interpreting underlying seasonality and event-based patterns (e.g., earnings season, Fed cycles)
    """
    )
