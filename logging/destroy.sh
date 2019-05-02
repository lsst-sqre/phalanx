#!/bin/bash
set -x

helm delete --purge ardent-ladybug
helm delete --purge nordic-bunny
helm delete --purge no-turkey

kubectl delete ingress -n logging kibana-ingress
