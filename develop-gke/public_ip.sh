#!/bin/bash -e

echo "Retrieving public IP of your LSST Science Platform..."

PUBLIC_IP=`kubectl get svc nginx-nginx-ingress-controller -n nginx --output jsonpath='{.status.loadBalancer.ingress[0].ip}'`

echo "Make sure your DNS points to this IP address:"
echo "$PUBLIC_IP"
