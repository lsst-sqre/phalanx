#!/bin/bash -e

ENVIRONMENT=${1:?"Usage: read_secrets.sh ENVIRONMENT"}

mkdir -p secrets

COMPONENTS=`vault kv list --format=yaml secret/k8s_operator/$ENVIRONMENT | yq -r '.[]'`
for SECRET in $COMPONENTS
do
  if [ $SECRET != "efd/" ] && [ $SECRET != "ts/" ]; then
    vault kv get --field=data --format=json secret/k8s_operator/$ENVIRONMENT/$SECRET > secrets/$SECRET
  fi
done
