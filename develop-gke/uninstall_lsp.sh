#!/bin/bash -x

echo "Starting uninstall of LSST Science Platform (develop-gke)..."

echo "Uninstalling Landing Page..."
helm delete --purge landing-page

echo "Uninstalling CADC TAP service..."
helm delete --purge tap

echo "Uninstalling Firefly..."
helm delete --purge firefly

echo "Uninstalling Nublado..."
helm delete --purge nublado

echo "Uninstalling Fileserver..."
helm delete --purge fileserver

echo "Finished uninstall of LSST Science Platform (develop-gke)..."
