#!/bin/sh
VALUES=$1
if [ -z "${VALUES}" ]; then
    VALUES="argo-cd"
fi
vfile="${VALUES}-values.yaml"
if ! [ -e "${vfile}" ]; then
    echo "No values file ${vfile}!" 1>&2
    exit 2
fi
helm install argo/argo-cd --namespace argocd --values ${vfile} --name argocd
