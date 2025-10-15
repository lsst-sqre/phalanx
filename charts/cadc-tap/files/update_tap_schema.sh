#!/bin/bash
set -euo pipefail

# ============================================================================
# Configuration and Logging
# ============================================================================

readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $*"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*"; }

# ============================================================================
# Validate Environment Variables
# ============================================================================

: "${SCHEMA_VERSION:?SCHEMA_VERSION is required}"
: "${SCHEMAS_TO_LOAD:?SCHEMAS_TO_LOAD is required}"
: "${PGHOST:?PGHOST is required}"
: "${PGDATABASE:?PGDATABASE is required}"

ENGINE_URL="postgresql://${PGUSER}:${PGPASSWORD}@${PGHOST}:${PGPORT}/${PGDATABASE}"
WORK_DIR="/tmp/work"
SCHEMA_DIR="${WORK_DIR}/schemas"

log_info "================================================"
log_info "TAP_SCHEMA Update: v${SCHEMA_VERSION}"
log_info "Schemas: ${SCHEMAS_TO_LOAD}"
log_info "Database: ${PGDATABASE}"
log_info "================================================"

# ============================================================================
# Wait for Database
# ============================================================================

log_info "Waiting for database connection..."
for i in {1..30}; do
    if psql -c "SELECT 1" > /dev/null 2>&1; then
        log_success "Database connection established"
        psql -c "SELECT version();" | head -3
        break
    fi

    if [[ $i -eq 30 ]]; then
        log_error "Failed to connect to database after 30 attempts"
        exit 1
    fi

    sleep 2
done

# ============================================================================
# Download Schemas
# ============================================================================

log_info "Downloading schemas from ${SCHEMA_VERSION}..."
mkdir -p "$SCHEMA_DIR"

GITHUB_URL="https://github.com/lsst/sdm_schemas/archive/refs/tags/${SCHEMA_VERSION}.tar.gz"
if ! curl -fsSL "$GITHUB_URL" | tar -xz -C "$SCHEMA_DIR"; then
    log_error "Failed to download or extract schemas from ${GITHUB_URL}"
    exit 1
fi

TOP_DIR=$(ls -1 "$SCHEMA_DIR" | head -1)
if [[ -z "$TOP_DIR" ]]; then
    log_error "No directory found in $SCHEMA_DIR"
    exit 1
fi

log_success "Detected top-level directory: $TOP_DIR"

# Build path to YAML files
YAML_DIR="${SCHEMA_DIR}/${TOP_DIR}/python/lsst/sdm/schemas"

if [[ ! -d "$YAML_DIR" ]]; then
    log_error "YAML directory not found at: $YAML_DIR"
    log_info "Contents of SCHEMA_DIR:"
    ls -la "$SCHEMA_DIR"
    exit 1
fi

log_success "Schemas available at: $YAML_DIR"

# ============================================================================
# Validate Requested Schemas
# ============================================================================

log_info "Validating requested schemas exist..."
IFS=',' read -ra SCHEMA_ARRAY <<< "$SCHEMAS_TO_LOAD"

for schema in "${SCHEMA_ARRAY[@]}"; do
    if [[ ! -f "${YAML_DIR}/${schema}.yaml" ]]; then
        log_error "Schema not found: ${schema}.yaml"
        log_info "Available schemas:"
        ls -1 "${YAML_DIR}"/*.yaml | xargs -n1 basename
        exit 1
    fi
    log_success "Found: ${schema}.yaml"
done

# ============================================================================
# Create staging and live TAP_SCHEMAS
# ============================================================================

log_info "Prepare schemas..."
psql -q -f /sql/prepare_schemas.sql
log_success "Schemas ready"

# ============================================================================
# Initialize TAP_SCHEMA Tables
# ============================================================================

log_info "Initializing TAP_SCHEMA tables..."

felis init-tap-schema \
    --engine-url="$ENGINE_URL" \
    --tap-schema-name="tap_schema_staging" \
    --extensions="/app/python/felis/config/tap_schema/tap_schema_extensions.yaml" \
    --tap-tables-postfix="11"

log_success "TAP_SCHEMA tables initialized"

# ============================================================================
# Create version table
# ============================================================================

log_info "Creating version table..."
psql -q -f /sql/create_version_table.sql
log_success "Version table ready"

# ============================================================================
# Load Schemas to Staging
# ============================================================================

log_info "Loading schemas to staging..."
for schema in "${SCHEMA_ARRAY[@]}"; do
    log_info "Loading ${schema}..."

    # Use Felis to load directly to database
    if felis load-tap-schema \
        --tap-schema-name=tap_schema_staging \
        --engine-url="$ENGINE_URL" \
        --tap-tables-postfix=11 \
        "${YAML_DIR}/${schema}.yaml"; then

        # Count what was loaded
        ROW_COUNT=$(psql -tAc "SELECT COUNT(*) FROM tap_schema_staging.schemas11 WHERE schema_name LIKE '%${schema}%'")
        log_success "Loaded ${schema} (${ROW_COUNT} schema entries)"
    else
        log_error "Failed to load ${schema}"
        exit 1
    fi
done

# ============================================================================
# Create Views
# ============================================================================

log_info "Creating views..."
psql -q -f /sql/create_views.sql
log_success "Views created"

# ============================================================================
# Swap staging & live TAP_SCHEMAS
# ============================================================================

log_info "Performing atomic schema swap..."
psql -q -f /sql/swap_schemas.sql
log_success "Schema swap complete - new schemas are now active"

# ============================================================================
# Record Version
# ============================================================================

log_info "Recording schema version..."
psql -q << EOF
INSERT INTO tap_schema.version (version, loaded_at)
VALUES ('${SCHEMA_VERSION}', CURRENT_TIMESTAMP)
ON CONFLICT (version) DO UPDATE
SET loaded_at = CURRENT_TIMESTAMP;
EOF
log_success "Version ${SCHEMA_VERSION} recorded"

# ============================================================================
# Validation and Summary
# ============================================================================

log_info "Validating loaded schemas..."
SCHEMA_COUNT=$(psql -tAc "SELECT COUNT(*) FROM tap_schema.schemas WHERE schema_name != 'tap_schema'")

if [[ "$SCHEMA_COUNT" -ge "${#SCHEMA_ARRAY[@]}" ]]; then
    log_success "Schema validation passed: ${SCHEMA_COUNT} schemas loaded"
else
    log_error "Expected at least ${#SCHEMA_ARRAY[@]} schemas, found ${SCHEMA_COUNT}"
    exit 1
fi

log_info "================================================"
log_success "TAP_SCHEMA Update Complete"
log_info "Version: ${SCHEMA_VERSION}"
log_info "Schemas: ${SCHEMA_COUNT} loaded"
log_info "================================================"

# Show what was loaded
psql -c "SELECT schema_name, description FROM tap_schema.schemas WHERE schema_name != 'tap_schema' ORDER BY schema_name;"

exit 0
