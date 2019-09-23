#!/bin/bash -ex

USAGE="Usage: ./install_ingress.sh FULLCHAIN_CERT_FILE PRIVATE_KEY"

CERT_FILE=${1:?$USAGE}
KEY_FILE=${2:?$USAGE}

echo "Starting install of the ingress for the LSST Science Platform..."

echo "Creating kubernetes secret with TLS certificate..."
echo "Certificate chain: $CERT_FILE"
echo "Private key file:  $KEY_FILE"
kubectl create secret tls tls-certificate --namespace default --cert $CERT_FILE --key $KEY_FILE

echo "Installing nginx-ingress..."
helm install stable/nginx-ingress --name nginx --namespace nginx --values nginx-ingress.yaml

echo "Now you can run the ./public_ip.sh script to get the IP address."
