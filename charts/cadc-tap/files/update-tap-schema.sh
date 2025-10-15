#!/bin/bash
set -e
set -o pipefail

echo "==========================================="
echo "TAP_SCHEMA Update Script"

echo "Schema Version: ${SCHEMA_VERSION}"
echo "Schemas to Load: ${SCHEMAS_TO_LOAD}"
echo "Database: ${PGDATABASE}"
echo "==========================================="

required_vars="SCHEMA_VERSION SCHEMAS_TO_LOAD PGHOST PGPORT PGDATABASE PGUSER PGPASSWORD"
for var in $required_vars; do
    if [ -z "${!var}" ]; then
        echo "ERROR: Required environment variable $var is not set"
        exit 1
    fi
done

echo "Testing database connection..."
if ! psql -h ${PGHOST} -p ${PGPORT} -U ${PGUSER} -d ${PGDATABASE} -c "SELECT version();" > /dev/null; then
    echo "ERROR: Cannot connect to database"
    exit 1
fi
echo "Database connection successful"

echo "Current schemas in database:"
psql -h ${PGHOST} -p ${PGPORT} -U ${PGUSER} -d ${PGDATABASE} -c "\dn"

echo ""
echo "==========================================="
echo " Script completed successfully"
echo "==========================================="
exit 0
