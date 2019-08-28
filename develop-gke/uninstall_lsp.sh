#!/bin/bash -x

echo "Starting uninstall of LSST Science Platform (develop-gke)..."

echo "Installing nginx-ingress..."
helm delete --purge lsp-nginx

echo "Finished uninstall of LSST Science Platform (develop-gke)..."
