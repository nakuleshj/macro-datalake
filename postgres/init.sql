CREATE TABLE IF NOT EXISTS silver_fred_cleaned (
    series_id TEXT, 
    date DATE, 
    value FLOAT, 
    frequency TEXT
    PRIMARY KEY (date, series_id)
);