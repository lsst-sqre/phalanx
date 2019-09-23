#!/bin/bash -ex

echo "Creating RBAC service account for tiller..."
kubectl create -f tiller/rbac-config.yaml

echo "Using helm to install tiller in cluster..."
helm init --service-account tiller --history-max 200
