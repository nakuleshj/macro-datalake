CREATE TABLE IF NOT EXISTS bronze_fred_raw (
    series_id TEXT,
    response JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS silver_fred_cleaned (
    series_id TEXT, 
    date DATE, 
    value FLOAT, 
    frequency TEXT
)