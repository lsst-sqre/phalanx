#!/bin/bash -e
USAGE="Usage: ./install.sh ENVIRONMENT VAULT_TOKEN"
ENVIRONMENT=${1:?$USAGE}
export VAULT_TOKEN=${2:?$USAGE}
export VAULT_ADDR=https://vault.lsst.codes
VAULT_PATH_PREFIX=`yq -r .vault_path_prefix ../science-platform/values-$ENVIRONMENT.yaml`
ARGOCD_PASSWORD=`vault kv get --field=argocd.admin.plaintext_password $VAULT_PATH_PREFIX/installer`

GIT_URL=`git config --get remote.origin.url`
# Github runs in a detached head state, but sets GITHUB_REF,
# extract the branch from it.  If we're there, use that branch.
# git branch --show-current will return empty in deatached head.
GIT_BRANCH=${GITHUB_HEAD_REF:-`git branch --show-current`}

echo "Set VAULT_TOKEN in a secret for vault-secrets-operator..."
# The namespace may not exist already, but don't error if it does.
kubectl create ns vault-secrets-operator || true
kubectl create secret generic vault-secrets-operator \
  --namespace vault-secrets-operator \
  --from-literal=VAULT_TOKEN=$VAULT_TOKEN \
  --from-literal=VAULT_TOKEN_LEASE_DURATION=31536000 \
  --dry-run=client -o yaml | kubectl apply -f -

echo "Set up docker pull secret for vault-secrets-operator..."
vault kv get --field=.dockerconfigjson $VAULT_PATH_PREFIX/pull-secret > docker-creds
kubectl create secret generic pull-secret -n vault-secrets-operator \
    --from-file=.dockerconfigjson=docker-creds \
    --type=kubernetes.io/dockerconfigjson \
    --dry-run=client -o yaml | kubectl apply -f -


echo "Update / install vault-secrets-operator..."
# ArgoCD depends on pull-secret, which depends on vault-secrets-operator.
helm dependency update ../services/vault-secrets-operator
helm upgrade vault-secrets-operator ../services/vault-secrets-operator \
  --install \
  --values ../services/vault-secrets-operator/values-$ENVIRONMENT.yaml \
  --create-namespace \
  --namespace vault-secrets-operator \
  --timeout 15m \
  --wait

echo "Update / install argocd using helm3..."
helm dependency update ../services/argocd
helm upgrade argocd ../services/argocd \
  --install \
  --values ../services/argocd/values-$ENVIRONMENT.yaml \
  --create-namespace \
  --namespace argocd \
  --timeout 15m \
  --wait

echo "Login to argocd..."
argocd login \
  --plaintext \
  --port-forward \
  --port-forward-namespace argocd \
  --username admin \
  --password $ARGOCD_PASSWORD

echo "Creating top level application"
argocd app create science-platform \
  --repo $GIT_URL \
  --path science-platform --dest-namespace default \
  --dest-server https://kubernetes.default.svc \
  --upsert \
  --revision $GIT_BRANCH \
  --port-forward \
  --port-forward-namespace argocd \
  --helm-set repoURL=$GIT_URL \
  --helm-set revision=$GIT_BRANCH \
  --values values-$ENVIRONMENT.yaml

argocd app sync science-platform \
  --port-forward \
  --port-forward-namespace argocd

echo "Syncing critical early applications"
if [ $(yq -r .ingress_nginx.enabled ../science-platform/values-$ENVIRONMENT.yaml) == "true" ];
then
  echo "Syncing ingress-nginx..."
  argocd app sync ingress-nginx \
    --port-forward \
    --port-forward-namespace argocd
fi

# Wait for the cert-manager's webhook to finish deploying by running
# kubectl, argocd's sync doesn't seem to wait for this to finish.
if [ $(yq -r .cert_manager.enabled ../science-platform/values-$ENVIRONMENT.yaml) == "true" ];
then
  echo "Syncing cert-manager..."
  argocd app sync cert-manager \
    --port-forward \
    --port-forward-namespace argocd && \
    kubectl -n cert-manager rollout status deploy/cert-manager-webhook
fi

if [ $(yq -r .postgres.enabled ../science-platform/values-$ENVIRONMENT.yaml) == "true" ];
then
  echo "Syncing postgres..."
  argocd app sync postgres \
    --port-forward \
    --port-forward-namespace argocd
fi

if [ $(yq -r .gafaelfawr.enabled ../science-platform/values-$ENVIRONMENT.yaml) == "true" ];
then
  echo "Syncing gafaelfawr..."
  argocd app sync gafaelfawr \
    --port-forward \
    --port-forward-namespace argocd
fi

echo "Sync remaining science platform apps"
argocd app sync -l "argocd.argoproj.io/instance=science-platform" \
  --port-forward \
  --port-forward-namespace argocd

echo "You can now check on your argo cd installation by running:"
echo "kubectl port-forward service/argocd-server -n argocd 8080:443"
echo "For the ArgoCD admin password:"
echo "vault kv get --field=argocd.admin.plaintext_password $VAULT_PATH_PREFIX/installer"
