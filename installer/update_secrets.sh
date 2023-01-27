#!/bin/bash -e
ENVIRONMENT=$1

export VAULT_DOC_UUID=`yq -r .onepassword_uuid ../science-platform/values.yaml`
VAULT_ADDR=${VAULT_ADDR:-https://vault.lsst.codes}
export VAULT_ADDR=$VAULT_ADDR
export VAULT_TOKEN=`./vault_key.py $ENVIRONMENT write`
export OP_CONNECT_HOST=https://roundtable.lsst.codes/1password

if [ -z "$OP_CONNECT_TOKEN" ]; then
    echo 'OP_CONNECT_TOKEN must be set to a 1Password Connect token' >&2
    exit 1
fi

echo "Clear out any existing secrets"
rm -rf secrets

echo "Reading current secrets from vault"
./read_secrets.sh $ENVIRONMENT

echo "Generating missing secrets with values from 1Password"
./generate_secrets.py $ENVIRONMENT --op

echo "Writing secrets to vault"
./write_secrets.sh $ENVIRONMENT
