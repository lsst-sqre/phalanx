-- Drop/recreate tap_schema_staging & create tap_schema

DROP SCHEMA IF EXISTS tap_schema_staging CASCADE;
CREATE SCHEMA IF NOT EXISTS tap_schema_staging;
CREATE SCHEMA IF NOT EXISTS tap_schema;
