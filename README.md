# MacroLake – U.S. Economic Intelligence Dashboard

**MacroLake** is a full-stack data engineering project built to give financial, economic, and strategy analysts a real-time view of the U.S. macroeconomy. It consolidates fragmented macroeconomic data into a unified, interactive dashboard that supports trend analysis, forecasting, and strategic decision-making.

## 🔧 Architecture Highlights

- **Data Lakehouse Design**  
  - **MinIO**: Object storage for raw & processed data (Bronze layer)  
  - **PostgreSQL**: Analytical serving layer (Gold layer)  

- **ETL & Orchestration**  
  - **Apache Airflow**: Scheduled ingestion from public APIs (e.g., FRED, BLS)  
  - **Pandas/SQL**: Data cleaning, transformation, and feature engineering  

- **Forecasting & Explainability**  
  - **Prophet, XGBoost**: Time series and economic forecasts  
  - **SHAP**: Model interpretability for feature impact  

- **Sentiment Analysis**  
  - **NLP tools (VADER/TextBlob)** on economic news and Fed speeches  
  - Sentiment scores and word clouds by macro topics (inflation, jobs, etc.)

- **Visualization**  
  - **Streamlit**: Real-time interactive dashboard with KPIs, drill-downs, forecasts, and sentiment tracking

## 🎯 Outcome

MacroLake provides analysts with a centralized, explainable, and continuously updated economic intelligence platform—streamlining research workflows and enabling faster, data-driven insights.

## Architecture

## Project Structure

## Tech Stack

## Features

## Setup Instructions

## How to Run

## Scheduled Jobs / Pipelines

## Sample Output / Dashboard

## EDA

## Data Sources

## Data Flow

## ML Models

## Tests / Data Validation

## Deployment

## Screenshots

## Future Improvements

## Author & Credits

## License
