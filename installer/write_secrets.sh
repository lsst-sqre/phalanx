#!/bin/bash -x

ENVIRONMENT=${1:?"Usage: write_secrets.sh ENVIRONMENT"}

# This is a bit tricky.  This makes the path different for
# $SECRET, which ends up getting passed into vault and making
# the keys.
cd secrets

for SECRET in *
do
  vault kv put secret/k8s_operator/$ENVIRONMENT/$SECRET @$SECRET
done
