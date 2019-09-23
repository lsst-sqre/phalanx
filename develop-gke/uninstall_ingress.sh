#!/bin/bash -x

echo "Uninstalling ingress for the LSST Science Platform (develop-gke)..."
echo "Uninstalling nginx-ingress..."
helm delete --purge nginx

echo "Deleting certificate secret..."
kubectl delete secret --namespace default tls-certificate
