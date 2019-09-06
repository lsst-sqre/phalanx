#!/bin/bash -ex

echo "Starting install of the ingress for the LSST Science Platform (develop-gke)..."

echo "Creating kubernetes secret with TLS certificate..."
kubectl create secret tls lsp-certificate --namespace lsp-nginx --cert $1 --key $2

echo "Installing nginx-ingress..."
helm install stable/nginx-ingress --name lsp-nginx --namespace nginx --values nginx-ingress.yaml

echo "Now you can run the ./public_ip script to get the IP address."
