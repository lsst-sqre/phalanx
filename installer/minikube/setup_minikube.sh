#!/bin/bash -xe

minikube start --driver=virtualbox --cpus=8 --memory=16g --disk-size=100g

# This allows us to point minikube.lsst.codes to the ingress-nginx controller.
# This is needed to allow for services inside the cluster to contact each
# other using the public name minikube.lsst.codes
kubectl apply -f coredns.yaml

# Restart coredns
kubectl scale deployment coredns --replicas=0 -n kube-system
kubectl scale deployment coredns --replicas=1 -n kube-system
