# MacroLake – U.S. Economic Intelligence Dashboard

**MacroLake** is a full-stack data engineering project built to give financial, economic, and strategy analysts a real-time view of the U.S. macroeconomy. It consolidates fragmented macroeconomic data into a unified, interactive dashboard that supports trend analysis, forecasting, and strategic decision-making.

## Tech Stack

**ETL & Orchestration**  
- **Apache Airflow** – DAG-based orchestration for scheduled ETL pipelines  
- **Pandas** – Extract, transform, and load logic
- **Public API** – FRED for real-time macroeconomic data  

**Storage & Architecture**  
- **MinIO** – Object storage for raw and processed datasets (Data Lake – Bronze layer)  
- **PostgreSQL** – Analytical database for cleaned, queryable data (Serving – Gold layer)  

**Time Series Forecasting**  
- **Prophet** – Forecasting the S&P 500 index value    

**Visualization & Interface**  
- **Streamlit** – Real-time dashboard with KPI cards, forecast visualizations, and multivariate exploration  

**Containerization & Deployment**  
- **Docker** – Containerized pipeline and app components  
- **Docker Compose** – Local multi-service orchestration

## Architecture
![alt text](https://github.com/nakuleshj/macro-datalake/blob/master/assets/Architecture_updated.png)

### Overview

This project implements a **modern, production-grade data pipeline** using the **Medallion architecture** with **Apache Airflow orchestration**, **MinIO as a data lake**, **PostgreSQL as the data warehouse**, and **Streamlit for interactive BI**.

### Data Source
**FRED (Federal Reserve Economic Data) API**: Fetches macroeconomic data (e.g., GDP, inflation, unemployment).

### Bronze Layer
- **MinIO**: Stores raw JSON/CSV from FRED.
- Acts as a Data Lake bucket.
- Data is not cleaned—pure dump from source.

### Silver Layer
- **PostgreSQL**: Loads cleaned & formatted data from Bronze.
- Data is parsed, type-corrected, deduplicated.
- Used for analytics or further transformations.

### Gold Layer
- **PostgreSQL**: Stores normalized, pivoted, and business-friendly datasets.
- Structured for efficient querying by analysts, ML pipelines, and dashboards.

### ML & BI Layer
**Streamlit**: Frontend dashboard that consumes data from the Gold Layer for ML & BI applications.
Enables:
- Summarizing Data
- EDA (Exploratory Data Analysis)
- Time series forecasting & visualizations

### Orchestration Layer (Apache Airflow DAGs)
1. `bronze_ingest_DAG`
  - Runs daily
  - Fetches data from FRED API
  - Saves it to MinIO (Bronze)
  - Triggers silver_transform_DAG
2. `silver_transform_DAG`
  - Reads from MinIO
  - Cleans and transforms the data
  - Writes to PostgreSQL (Silver)
  - Triggers gold_optimize_DAG
3. `gold_optimize_DAG`
  - Reads Silver data
  - Normalizes, pivots, aggregates
  - Writes to PostgreSQL (Gold)
  - Triggers export_gold_data_DAG
4. `export_gold_data_DAG`
  - Exports final tables for consumption
  - Streamlit connects to this layer

## Prerequisites
- [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [Docker](https://www.docker.com/get-started/)

## How to Run

## Deployment

## Screenshots

## Future Improvements

## License
