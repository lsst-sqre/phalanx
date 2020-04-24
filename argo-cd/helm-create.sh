#!/bin/sh
helm init
kubectl create namespace argocd
kubectl create serviceaccount tiller --namespace kube-system
kubectl create -f tiller-clusterrolebinding.yaml
helm init --service-account tiller --upgrade
./create.sh $1
