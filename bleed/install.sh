#!/bin/bash -ex
USAGE="Usage: ./install.sh ENVIRONMENT VAULT_TOKEN FULLCHAIN_CERT_FILE PRIVATE_KEY [REVISION]"
ENVIRONMENT=${1:?$USAGE}
VAULT_TOKEN=${2:?$USAGE}
CERT_FILE=${3:?$USAGE}
KEY_FILE=${4:?$USAGE}
REVISION=${5:-HEAD}

echo "Creating initial resources (like RBAC service account for tiller)..."
kubectl apply -f initial-resources.yaml

echo "Using helm to install tiller in cluster..."
helm init --service-account tiller --history-max 200 --wait --upgrade

echo "Add the argocd helm update..."
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update

echo "Update / install argocd using helm..."
helm upgrade \
  --install argocd argo/argo-cd \
  --values argo-cd-values.yaml \
  --namespace argocd \
  --wait --timeout 900

echo "Creating vault secret..."
kubectl create secret generic vault-secrets-operator \
  --namespace vault-secrets-operator \
  --from-literal=VAULT_TOKEN=$VAULT_TOKEN \
  --from-literal=VAULT_TOKEN_LEASE_DURATION=86400 \
  --dry-run -o yaml | kubectl apply -f -

echo "Creating TLS secret..."
kubectl create secret tls tls-certificate \
  --namespace default \
  --cert $CERT_FILE \
  --key $KEY_FILE \
  --dry-run -o yaml | kubectl apply -f -

echo "Login to argocd..."
ARGOCD_PASSWORD=`kubectl get pods \
  --template '{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}' \
  --namespace argocd | grep argocd-server`

argocd login \
  --plaintext \
  --port-forward \
  --port-forward-namespace argocd \
  --username admin \
  --password $ARGOCD_PASSWORD

echo "Create vault secrets operator..."
argocd app create vault-secrets-operator \
  --repo https://github.com/lsst-sqre/lsp-deploy.git \
  --path services/vault-secrets-operator \
  --dest-namespace vault-secrets-operator \
  --dest-server https://kubernetes.default.svc \
  --upsert \
  --port-forward \
  --port-forward-namespace argocd

argocd app sync vault-secrets-operator \
  --port-forward \
  --port-forward-namespace argocd

echo "Creating top level application"
argocd app create science-platform \
  --repo https://github.com/lsst-sqre/lsp-deploy.git \
  --path science-platform --dest-namespace default \
  --dest-server https://kubernetes.default.svc \
  --upsert \
  --revision $REVISION \
  --port-forward \
  --port-forward-namespace argocd \
  --values values-$ENVIRONMENT.yaml

argocd app sync science-platform \
  --port-forward \
  --port-forward-namespace argocd

echo "Sync science platform apps"
argocd app sync -l "argocd.argoproj.io/instance=science-platform" \
  --port-forward \
  --port-forward-namespace argocd

echo "You can now check on your argo cd installation by running:"
echo "kubectl port-forward service/argocd-server -n argocd 8080:443"
echo "Login with username: admin password: $ARGOCD_PASSWORD"
