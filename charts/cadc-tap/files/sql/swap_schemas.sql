-- Atomic three-way swap

BEGIN;
ALTER SCHEMA tap_schema RENAME TO tap_schema_temp;
ALTER SCHEMA tap_schema_staging RENAME TO tap_schema;
ALTER SCHEMA tap_schema_temp RENAME TO tap_schema_staging;
COMMIT;
