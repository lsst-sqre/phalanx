#!/bin/bash
set -ex

helm install stable/elasticsearch --name nordic-bunny --namespace logging --values es-values.yaml
helm install kiwigrid/fluentd-elasticsearch --name no-turkey --values fluentd-es-values.yaml --namespace logging
helm install stable/kibana --name ardent-ladybug --values kibana-values.yaml --namespace logging
kubectl create -f ingress-int.yaml --namespace logging
