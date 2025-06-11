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

CREATE TABLE IF NOT EXISTS dim_date (
    date_id DATE PRIMARY KEY,
    year INT,
    quarter INT,
    month INT
)

CREATE TABLE IF NOT EXISTS dim_series(
    series_id TEXT PRIMARY KEY,
    title TEXT,
    units TEXT,
    seasonal_adjustment TEXT
);

CREATE TABLE IF NOT EXISTS dim_location(
    location_id TEXT PRIMARY KEY,  
    region_name TEXT
);

CREATE TABLE IF NOT EXISTS dim_frequency(
    frequency TEXT PRIMARY KEY,
    description TEXT
);

CREATE TABLE IF NOT EXISTS fact_macro_features(
    date_id DATE REFERENCES dim_date(date_id),
    series_id TEXT REFERENCES dim_series(series_id),
    location_id TEXT REFERENCES dim_location(location_id),
    frequency TEXT REFERENCES dim_frequency(frequency),
    value FLOAT,
    yoy_growth FLOAT,
    ma_3mo FLOAT,
    ma_6mo FLOAT,
    recession_flag INT,
    PRIMARY KEY (date_id, series_id)
);