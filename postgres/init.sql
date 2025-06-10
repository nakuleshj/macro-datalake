CREATE TABLE bronze_fred_raw IF NOT EXISTS (
    series_id TEXT,
    response JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
)