CREATE TABLE IF NOT EXISTS bronze_fred_raw (
    series_id TEXT,
    response JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);