#!/bin/bash
set -euo pipefail

echo "=== TAP_SCHEMA Update Script ==="
echo "SCHEMA_VERSION: ${SCHEMA_VERSION}"
echo "SCHEMAS_TO_LOAD: ${SCHEMAS_TO_LOAD}"
echo "PGHOST: ${PGHOST}"
echo "PGDATABASE: ${PGDATABASE}"
echo "GCS_BUCKET: ${GCS_BUCKET}"

# ------------------------------------------------------------------------
# Step 0: Prepare working directories
# ------------------------------------------------------------------------
WORK_DIR="${WORK_DIR:-/tmp/work}"
SCHEMA_DIR="${SCHEMA_DIR:-${WORK_DIR}/schemas}"
SQL_DIR="${SQL_DIR:-${WORK_DIR}/sql}"

mkdir -p "${WORK_DIR}" "${SCHEMA_DIR}" "${SQL_DIR}"
echo "Working directories initialized:"
echo "  WORK_DIR=${WORK_DIR}"
echo "  SCHEMA_DIR=${SCHEMA_DIR}"
echo "  SQL_DIR=${SQL_DIR}"
echo ""

MAX_ATTEMPTS=30
ATTEMPT=0
while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
  ATTEMPT=$((ATTEMPT + 1))
  if psql -h "${PGHOST}" -p "${PGPORT}" -U "${PGUSER}" -d "${PGDATABASE}" -c "SELECT 1;" >/dev/null 2>&1; then
    break
  fi
  echo "Waiting for database... attempt ${ATTEMPT}/${MAX_ATTEMPTS}"
  sleep 2

  if [ $ATTEMPT -eq $MAX_ATTEMPTS ]; then
    echo "ERROR: Failed to connect to database after ${MAX_ATTEMPTS} attempts"
    ps aux | grep cloud_sql_proxy || true
    netstat -ln | grep 5432 || true
    exit 1
  fi
done

echo "Testing database connection..."
psql -h "${PGHOST}" -p "${PGPORT}" -U "${PGUSER}" -d "${PGDATABASE}" -c "SELECT version();" || {
  echo "ERROR: Database connection failed"
  exit 1
}
echo "Database connection successful"
echo ""

echo "=== Step 2: Downloading schemas ==="
SCHEMA_TARBALL="schemas-${SCHEMA_VERSION}.tar.gz"
GCS_URL="https://github.com/lsst/sdm_schemas/archive/refs/tags/w.2025.42.tar.gz"

echo "Downloading from: ${GCS_URL}"
curl -f -L -o "${WORK_DIR}/${SCHEMA_TARBALL}" "${GCS_URL}" || {
  echo "ERROR: Failed to download schema tarball from GCS"
  echo "URL: ${GCS_URL}"
  exit 1
}

echo "Extracting schemas..."
tar -xzf "${WORK_DIR}/${SCHEMA_TARBALL}" -C "${SCHEMA_DIR}" || {
  echo "ERROR: Failed to extract schema tarball"
  exit 1
}

echo "Detecting extracted top-level directory..."
TOP_DIR=$(tar -tzf "${WORK_DIR}/${SCHEMA_TARBALL}" 2>/dev/null | head -1 | cut -d/ -f1 || true)

if [ -n "${TOP_DIR}" ] && [ -d "${SCHEMA_DIR}/${TOP_DIR}/python/lsst/sdm/schemas" ]; then
  echo "Detected top-level directory: ${TOP_DIR}"
  SCHEMA_DIR="${SCHEMA_DIR}/${TOP_DIR}"
else
  echo "WARNING: Could not detect expected schema directory. Listing contents of ${SCHEMA_DIR}:"
  ls -la "${SCHEMA_DIR}" || true
fi

echo "Available schemas:"
ls -la "${SCHEMA_DIR}/python/lsst/sdm/schemas/" || ls -la "${SCHEMA_DIR}/"
echo ""

echo "=== Step 3: Validating requested schemas ==="
IFS=',' read -ra SCHEMA_ARRAY <<< "$SCHEMAS_TO_LOAD"
for schema_name in "${SCHEMA_ARRAY[@]}"; do
  schema_name=$(echo "$schema_name" | tr -d ' ')
  schema_file="${SCHEMA_DIR}/python/lsst/sdm/schemas/${schema_name}.yaml"

  if [ ! -f "${schema_file}" ]; then
    echo "ERROR: Schema file not found: ${schema_file}"
    echo "Available schemas in yml directory:"
    ls ${SCHEMA_DIR}/python/lsst/sdm/schemas/*.yaml 2>/dev/null || echo "No yaml files found"
    exit 1
  fi
  echo "Found schema: ${schema_name}.yaml"
done
echo ""

echo "=== Step 4: Validating schemas with Felis ==="
for schema_name in "${SCHEMA_ARRAY[@]}"; do
  schema_name=$(echo "$schema_name" | tr -d ' ')
  schema_file="${SCHEMA_DIR}/python/lsst/sdm/schemas/${schema_name}.yaml"
  echo "Validating ${schema_name}..."
  felis validate --check-description "${schema_file}" || {
    echo "ERROR: Schema validation failed for ${schema_name}"
    exit 1
  }
done
echo "All schemas validated successfully"
echo ""

echo "=== Step 5: Checking TAP_SCHEMA initialization ==="

SCHEMA_EXISTS=$(psql -h "${PGHOST}" -p "${PGPORT}" -U "${PGUSER}" -d "${PGDATABASE}" -tAc \
  "SELECT 1 FROM information_schema.schemata WHERE schema_name = 'tap_schema';")

STAGING_EXISTS=$(psql -h "${PGHOST}" -p "${PGPORT}" -U "${PGUSER}" -d "${PGDATABASE}" -tAc \
  "SELECT 1 FROM information_schema.schemata WHERE schema_name = 'tap_schema_staging';")

if [ "$SCHEMA_EXISTS" != "1" ]; then
  echo "Creating tap_schema..."
  psql -h "${PGHOST}" -p "${PGPORT}" -U "${PGUSER}" -d "${PGDATABASE}" -c "CREATE SCHEMA IF NOT EXISTS tap_schema;"
  echo "Initializing TAP_SCHEMA tables..."
  felis init-tap-schema \
    --engine-url="postgresql://${PGUSER}@${PGHOST}:${PGPORT}/${PGDATABASE}" \
    --tap-schema-name=tap_schema || {
    echo "ERROR: Failed to initialize tap_schema"
    exit 1
  }
else
  echo "tap_schema already exists"
fi

if [ "$STAGING_EXISTS" != "1" ]; then
  echo "Creating tap_schema_staging..."
  psql -h "${PGHOST}" -p "${PGPORT}" -U "${PGUSER}" -d "${PGDATABASE}" -c "CREATE SCHEMA IF NOT EXISTS tap_schema_staging;"
  echo "Initializing TAP_SCHEMA staging tables..."
  felis init-tap-schema \
    --engine-url="postgresql://${PGUSER}@${PGHOST}:${PGPORT}/${PGDATABASE}" \
    --tap-schema-name=tap_schema_staging || {
    echo "ERROR: Failed to initialize tap_schema_staging"
    exit 1
  }
else
  echo "tap_schema_staging already exists"
fi
echo ""

echo "=== Step 6: Generating SQL files for schemas ==="
echo "-- Clear staging schema data" > "${SQL_DIR}/01_clear_staging.sql"
cat >> "${SQL_DIR}/01_clear_staging.sql" << 'EOF'
DELETE FROM tap_schema_staging.key_columns;
DELETE FROM tap_schema_staging.keys;
DELETE FROM tap_schema_staging.columns;
DELETE FROM tap_schema_staging.tables;
DELETE FROM tap_schema_staging.schemas;
EOF

echo "Generated: ${SQL_DIR}/01_clear_staging.sql"

COUNTER=2
for schema_name in "${SCHEMA_ARRAY[@]}"; do
  schema_name=$(echo "$schema_name" | tr -d ' ')
  schema_file="${SCHEMA_DIR}/python/lsst/sdm/schemas/${schema_name}.yaml"
  sql_file="${SQL_DIR}/$(printf "%02d" $COUNTER)_load_${schema_name}.sql"

  echo "Generating SQL for ${schema_name}..."
  felis load-tap-schema \
    --dry-run \
    --output-file="${sql_file}" \
    --tap-schema-name=tap_schema_staging \
    --engine-url="postgresql://${PGUSER}@${PGHOST}:${PGPORT}/${PGDATABASE}" \
    "${schema_file}" || {
    echo "ERROR: Failed to generate SQL for ${schema_name}"
    exit 1
  }

  echo "Generated: ${sql_file}"
  echo "First 10 lines:"
  head -n 10 "${sql_file}" || true
  echo "..."
  echo "Total lines: $(wc -l < "${sql_file}")"
  COUNTER=$((COUNTER + 1))
done

echo "-- Atomic schema swap" > "${SQL_DIR}/99_swap_schemas.sql"
cat >> "${SQL_DIR}/99_swap_schemas.sql" << 'EOF'
BEGIN;
ALTER SCHEMA tap_schema RENAME TO tap_schema_temp;
ALTER SCHEMA tap_schema_staging RENAME TO tap_schema;
ALTER SCHEMA tap_schema_temp RENAME TO tap_schema_staging;
COMMIT;
EOF

echo "Generated: ${SQL_DIR}/99_swap_schemas.sql"
echo ""

echo "=== Step 7: SQL Execution Plan ==="
echo "The following SQL files would be executed in order:"
ls -1 "${SQL_DIR}"/*.sql | sort
echo ""
echo "=== Summary ==="
echo "Successfully generated SQL files for schemas: ${SCHEMAS_TO_LOAD}"
echo "SQL files are in: ${SQL_DIR}"
echo "TAP_SCHEMA update script completed successfully."
exit 0
