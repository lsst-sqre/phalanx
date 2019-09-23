#!/bin/bash -ex

echo "Starting install of LSST Science Platform (develop-gke)..."

echo "Updating helm charts from repository..."

# Use this line to develop charts locally.
#helm repo add lsstsqre http://localhost:8879

# Use public charts on github
helm repo add lsstsqre https://lsst-sqre.github.io/charts/

helm repo update

echo "Installing Fileserver..."
helm install lsstsqre/fileserver --name fileserver --namespace fileserver

echo "Installing Landing Page..."
helm install lsstsqre/landing-page --name landing-page --namespace landing-page

echo "Installing CADC TAP service..."
helm install lsstsqre/cadc-tap --name tap --namespace tap

echo "Installing Firefly..."
helm install lsstsqre/firefly --name firefly --namespace firefly

echo "Installing Nublado..."
helm install lsstsqre/nublado --name nublado --namespace nublado --values nublado-values.yaml

echo "Success!  It make take a few moments to start all the services."
