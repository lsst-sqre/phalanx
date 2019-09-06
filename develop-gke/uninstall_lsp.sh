#!/bin/bash -x

echo "Starting uninstall of LSST Science Platform (develop-gke)..."

echo "Uninstalling TAP service..."
helm delete --purge lsp-tap

echo "Finished uninstall of LSST Science Platform (develop-gke)..."
