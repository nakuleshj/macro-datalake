# MacroLake – U.S. Economic Intelligence Dashboard

**MacroLake** is a full-stack data engineering project built to give financial, economic, and strategy analysts a real-time view of the U.S. macroeconomy. It consolidates fragmented macroeconomic data into a unified, interactive dashboard that supports trend analysis, forecasting, and strategic decision-making.

## Architecture

## Project Structure

## Tech Stack

**Data Ingestion & Orchestration**  
- **Apache Airflow** – DAG-based orchestration for scheduled ETL pipelines  
- **Python** – Data processing, forecasting, and backend logic  
- **Public APIs** – FRED, BLS, NewsAPI for real-time macroeconomic and sentiment data  

**Storage & Architecture**  
- **MinIO** – Object storage for raw and processed datasets (Data Lake – Bronze layer)  
- **PostgreSQL** – Analytical database for cleaned, queryable data (Serving – Gold layer)  

**Machine Learning & Forecasting**  
- **Prophet** – Time series forecasting (GDP, CPI, Unemployment)  
- **XGBoost** – Supervised learning for forward-looking economic models  
- **SHAP** – Model explainability via feature importance plots  

**NLP & Sentiment Analysis**  
- **VADER/TextBlob** – Rule-based sentiment scoring of economic news and Fed speeches  

**Visualization & Interface**  
- **Streamlit** – Real-time dashboard with KPI cards, forecast visualizations, sentiment views, and multivariate exploration  

**Containerization & Deployment**  
- **Docker** – Containerized pipeline and app components  
- **Docker Compose** – Local multi-service orchestration  

## Features

### U.S. Economic Summary
- KPI cards for GDP growth, Inflation (CPI/Core CPI), Unemployment Rate, and Fed Funds Rate
- Sparkline trends with last 12–24 months of data
- “Latest Release” badges with direct source links
- Macro health bar visualizing current risk levels

### Economic Indicators Explorer
- Drill down into indicators like GDP, CPI, Retail Sales, Industrial Production, etc.
- Line charts with MoM/YoY overlays
- Recession band annotations (NBER)
- Comparison mode to overlay multiple indicators

### Forecasts & Drivers
- ML forecasts using Prophet and XGBoost for key indicators
- 95% confidence interval visualizations
- SHAP plots to explain feature contributions to forecasts
- Risk gauges (e.g., “Inflation Overheat: High”)

### News & Policy Sentiment
- Real-time sentiment tracking from NewsAPI and Fed speeches
- Rolling sentiment timeline by topic
- Word clouds for inflation, labor, housing, etc.
- Latest headlines table with sentiment scores

### Business & Policy Insights
- GPT-style summaries of economic shifts (last 7 days)
- Top 3 macro risks impacting markets or sectors
- Suggested implications for decision-makers

### Multivariate Macro Explorer
- Correlation matrix (Pearson, Spearman)
- PCA projection for dimensionality reduction
- Scatter plots (e.g., Inflation vs Wage Growth)

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
