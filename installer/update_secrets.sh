#!/bin/bash -e
ENVIRONMENT=$1

export VAULT_DOC_UUID=`yq -r .onepassword_uuid ../science-platform/values.yaml`
export VAULT_ADDR=https://vault.lsst.codes
export VAULT_TOKEN=`./vault_key.py $ENVIRONMENT write`

echo "Clear out any existing secrets"
rm -rf secrets

echo "Reading current secrets from vault"
./read_secrets.sh $ENVIRONMENT

echo "Generating missing secrets with values from onepassword"
./generate_secrets.py $ENVIRONMENT --op

echo "Writing secrets to vault"
./write_secrets.sh $ENVIRONMENT
