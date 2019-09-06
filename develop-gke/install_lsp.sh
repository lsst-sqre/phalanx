#!/bin/bash -ex

echo "Starting install of LSST Science Platform (develop-gke)..."

echo "Updating helm charts from repository..."
helm repo add lsstsqre http://localhost:8879
#helm repo add lsstsqre https://lsst-sqre.github.io/charts/
helm repo update

echo "Installing TAP service..."
helm install lsstsqre/cadc-tap --name lsp-tap --namespace tap
