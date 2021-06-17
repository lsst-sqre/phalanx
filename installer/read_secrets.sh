#!/bin/bash -e

ENVIRONMENT=${1:?"Usage: read_secrets.sh ENVIRONMENT"}
PREFIX=${VAULT_PATH:-secret/k8s_operator/$ENVIRONMENT}

mkdir -p secrets

COMPONENTS=`vault kv list --format=yaml $VAULT_PATH | yq -r '.[]'`
for SECRET in $COMPONENTS
do
  if [ $SECRET != "efd/" ] && [ $SECRET != "ts/" ]; then
    vault kv get --field=data --format=json $VAULT_PATH/$SECRET > secrets/$SECRET
  fi
done
