-- Create views pointing to *11 tables

CREATE OR REPLACE VIEW tap_schema_staging.schemas AS SELECT * FROM tap_schema_staging.schemas11;
CREATE OR REPLACE VIEW tap_schema_staging.tables AS SELECT * FROM tap_schema_staging.tables11;
CREATE OR REPLACE VIEW tap_schema_staging.columns AS SELECT * FROM tap_schema_staging.columns11;
CREATE OR REPLACE VIEW tap_schema_staging.keys AS SELECT * FROM tap_schema_staging.keys11;
CREATE OR REPLACE VIEW tap_schema_staging.key_columns AS SELECT * FROM tap_schema_staging.key_columns11;
CREATE OR REPLACE VIEW tap_schema_staging.version AS SELECT * FROM tap_schema_staging.version11;

-- Create views in tap_schema

CREATE OR REPLACE VIEW tap_schema.schemas AS SELECT * FROM tap_schema.schemas11;
CREATE OR REPLACE VIEW tap_schema.tables AS SELECT * FROM tap_schema.tables11;
CREATE OR REPLACE VIEW tap_schema.columns AS SELECT * FROM tap_schema.columns11;
CREATE OR REPLACE VIEW tap_schema.keys AS SELECT * FROM tap_schema.keys11;
CREATE OR REPLACE VIEW tap_schema.key_columns AS SELECT * FROM tap_schema.key_columns11;
CREATE OR REPLACE VIEW tap_schema.version AS SELECT * FROM tap_schema.version11;
