#!/bin/bash -ex
ENVIRONMENT=$1

export VAULT_DOC_UUID=`yq -r .onepassword_uuid ../science-platform/values.yaml`
export VAULT_ADDR=https://vault.lsst.codes
export VAULT_TOKEN=`./vault_key.py $ENVIRONMENT write`

./read_secrets.sh $ENVIRONMENT
./generate_secrets.py $ENVIRONMENT --op
./write_secrets.sh $ENVIRONMENT
