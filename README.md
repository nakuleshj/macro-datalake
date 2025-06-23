# MacroLake – U.S. Economic Intelligence Dashboard

**MacroLake** is a full-stack data engineering project built to give financial, economic, and strategy analysts a real-time view of the U.S. macroeconomy. It consolidates fragmented macroeconomic data into a unified, interactive dashboard that supports trend analysis, forecasting, and strategic decision-making.

## Architecture
![alt text](https://github.com/nakuleshj/macro-datalake/blob/master/assets/Architecture.png)

## Tech Stack

**Data Ingestion & Orchestration**  
- **Apache Airflow** – DAG-based orchestration for scheduled ETL pipelines  
- **Python** – Data processing, forecasting, and backend logic  
- **Public APIs** – FRED, BLS, NewsAPI for real-time macroeconomic and sentiment data  

**Storage & Architecture**  
- **MinIO** – Object storage for raw and processed datasets (Data Lake – Bronze layer)  
- **PostgreSQL** – Analytical database for cleaned, queryable data (Serving – Gold layer)  

**Machine Learning**  
- **Prophet** – Time series forecasting (S&P 500)  

**NLP & Sentiment Analysis**  
- **VADER/TextBlob** – Rule-based sentiment scoring of economic news and Fed speeches  

**Visualization & Interface**  
- **Streamlit** – Real-time dashboard with KPI cards, forecast visualizations, and multivariate exploration  

**Containerization & Deployment**  
- **Docker** – Containerized pipeline and app components  
- **Docker Compose** – Local multi-service orchestration  

## Setup Instructions

## How to Run


## Sample Output / Dashboard



## Deployment

## Screenshots

## Future Improvements

## Author & Credits

## License
