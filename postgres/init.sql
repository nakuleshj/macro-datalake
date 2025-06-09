CREATE TABLE broze_fred_raw IF NOT EXISTS (
    series_id TEXT,
    response JSONB,
    timestamp TIMESTAMPZ,
)