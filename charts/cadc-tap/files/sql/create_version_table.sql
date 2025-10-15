-- Create version table

CREATE TABLE IF NOT EXISTS tap_schema_staging.version11 (
    version TEXT PRIMARY KEY,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
