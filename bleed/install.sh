#!/bin/bash -ex
USAGE="Usage: ./install.sh VAULT_TOKEN FULLCHAIN_CERT_FILE PRIVATE_KEY"
VAULT_TOKEN=${1:?$USAGE}
CERT_FILE=${2:?$USAGE}
KEY_FILE=${3:?$USAGE}

echo "Creating initial resources (like RBAC service account for tiller)..."
kubectl apply -f initial-resources.yaml

echo "Using helm to install tiller in cluster..."
helm init --service-account tiller --history-max 200

echo "Add the argocd helm update..."
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update

echo "Update / install argocd using helm..."
helm upgrade --install argocd argo/argo-cd --values argo-cd-values.yaml --namespace argocd

echo "Creating vault secret..."
kubectl create secret generic vault-secrets-operator -n vault-secrets-operator --from-literal=VAULT_TOKEN=$VAULT_TOKEN --from-literal=VAULT_TOKEN_LEASE_DURATION=86400 --dry-run -o yaml | kubectl apply -f -

echo "Creating TLS secret..."
kubectl create secret tls tls-certificate --namespace default --cert $CERT_FILE --key $KEY_FILE --dry-run -o yaml | kubectl apply -f -

echo "Login to argocd..."
kubectl port-forward service/argocd-server -n argocd 8080:443 &
ARGOCD_PASSWORD=`kubectl get pods --template '{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}' -n argocd | grep argocd-server`
sleep 5
argocd login localhost:8080 --insecure --password $ARGOCD_PASSWORD --username admin

echo "Create argocd apps..."
argocd app create vault-secrets-operator --repo https://github.com/lsst-sqre/lsp-deploy.git --path services/vault-secrets-operator --dest-namespace vault-secrets-operator --dest-server https://kubernetes.default.svc --upsert --sync-policy automated

argocd app create nginx-ingress --repo https://kubernetes-charts.storage.googleapis.com --helm-chart nginx-ingress --revision 1.26.1 --dest-namespace nginx-ingress --dest-server https://kubernetes.default.svc --upsert --sync-policy automated --helm-set controller.extraArgs.default-ssl-certificate=default/tls-certificate --helm-set controller.service.omitClusterIP=true,controller.stats.service.omitClusterIP=true,controller.metrics.service.omitClusterIP=true,defaultBackend.service.omitClusterIP=true

argocd app create science-platform --repo https://github.com/lsst-sqre/lsp-deploy.git --path science-platform --dest-namespace default --dest-server https://kubernetes.default.svc --upsert --sync-policy automated
