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



## Prerequisites
- [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [Docker](https://www.docker.com/get-started/)

## How to Run


## Sample Output / Dashboard



## Deployment

## Screenshots

## Future Improvements

## Author & Credits

## License
