helm delete --purge argocd
kubectl delete crd -l app.kubernetes.io/part-of=argocd
