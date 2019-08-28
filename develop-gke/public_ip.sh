#!/bin/bash -e

echo "Retrieving public IP of your LSST Science Platform..."
PUBLIC_IP=`kubectl get svc lsp-nginx-nginx-ingress-controller -n nginx --output jsonpath='{.status.loadBalancer.ingress[0].ip}'`

echo "$PUBLIC_IP"
