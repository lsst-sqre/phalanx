#!/bin/bash -e
USAGE="Usage: ./install.sh ENVIRONMENT VAULT_ROLE_ID VAULT_SECRET_ID"
ENVIRONMENT=${1:?$USAGE}
config="../environments/values-${ENVIRONMENT}.yaml"
VAULT_ROLE_ID=${2:?$USAGE}
VAULT_SECRET_ID=${3:?$USAGE}

echo "Getting Git branch and remote information..."
GIT_URL=$(git config --get remote.origin.url)
# Github runs in a detached head state, but sets GITHUB_REF,
# extract the branch from it.  If we're there, use that branch.
# git branch --show-current will return empty in deatached head.
GIT_BRANCH=${GITHUB_HEAD_REF:-$(git branch --show-current)}

echo "Logging on to Vault..."
if grep '^vaultUrl:' "$config" >/dev/null; then
    export VAULT_ADDR=$(yq -r .vaultUrl "$config")
else
    export VAULT_ADDR=$(yq -r .vaultUrl ../environments/values.yaml)
fi
export VAULT_TOKEN=$(vault write auth/approle/login role_id="$VAULT_ROLE_ID" secret_id="$VAULT_SECRET_ID" | grep 'token ' | awk '{ print $2 }')
VAULT_PATH_PREFIX=$(yq -r .vaultPathPrefix "$config")
ARGOCD_PASSWORD=$(vault kv get --field=admin.plaintext_password "$VAULT_PATH_PREFIX"/argocd)

echo "Putting Vault credentials in a secret for vault-secrets-operator..."
# The namespace may not exist already, but don't error if it does.
kubectl create ns vault-secrets-operator || true
kubectl create secret generic vault-credentials \
  --namespace vault-secrets-operator \
  --from-literal=VAULT_ROLE_ID="$VAULT_ROLE_ID" \
  --from-literal=VAULT_SECRET_ID="$VAULT_SECRET_ID" \
  --dry-run=client -o yaml | kubectl apply -f -

# Argo CD depends a Vault-created secret for its credentials, so
# vault-secrets-operator has to be installed first.
echo "Updating or installing vault-secrets-operator..."
helm dependency update ../applications/vault-secrets-operator
helm upgrade vault-secrets-operator ../applications/vault-secrets-operator \
  --install \
  --values ../applications/vault-secrets-operator/values.yaml \
  --values ../applications/vault-secrets-operator/values-$ENVIRONMENT.yaml \
  --set vault-secrets-operator.vault.address="$VAULT_ADDR" \
  --create-namespace \
  --namespace vault-secrets-operator \
  --timeout 5m \
  --wait

echo "Updating or installing Argo CD using Helm..."
helm dependency update ../applications/argocd
helm upgrade argocd ../applications/argocd \
  --install \
  --values ../applications/argocd/values.yaml \
  --values ../applications/argocd/values-$ENVIRONMENT.yaml \
  --set global.vaultSecretsPath="$VAULT_PATH_PREFIX" \
  --create-namespace \
  --namespace argocd \
  --timeout 5m \
  --wait

echo "Logging in to Argo CD..."
argocd login \
  --plaintext \
  --port-forward \
  --port-forward-namespace argocd \
  --username admin \
  --password $ARGOCD_PASSWORD

echo "Creating the top-level Argo CD application..."
argocd app create science-platform \
  --repo "$GIT_URL" \
  --path environments --dest-namespace default \
  --dest-server https://kubernetes.default.svc \
  --upsert \
  --revision "$GIT_BRANCH" \
  --port-forward \
  --port-forward-namespace argocd \
  --helm-set repoUrl="$GIT_URL" \
  --helm-set targetRevision="$GIT_BRANCH" \
  --values values.yaml \
  --values values-$ENVIRONMENT.yaml

echo "Syncing the top-level Argo CD application..."
argocd app sync science-platform \
  --port-forward \
  --port-forward-namespace argocd

if [ $(yq -r '.applications."ingress-nginx"' "$config") != "false" ]; then
  echo "Syncing ingress-nginx..."
  argocd app sync ingress-nginx \
    --port-forward \
    --port-forward-namespace argocd
fi

if [ $(yq -r '.applications."cert-manager"' "$config") != "false" ]; then
  echo "Syncing cert-manager..."
  argocd app sync cert-manager \
    --port-forward \
    --port-forward-namespace argocd && \

  # Wait for the cert-manager's webhook to finish deploying by running
  # kubectl, argocd's sync doesn't seem to wait for this to finish.
  kubectl -n cert-manager rollout status deploy/cert-manager-webhook
fi

if [ $(yq -r .applications.postgres "$config") == "true" ]; then
  echo "Syncing postgres..."
  argocd app sync postgres \
    --port-forward \
    --port-forward-namespace argocd
fi

if [ $(yq -r .applications.gafaelfawr "$config") != "false" ]; then
  echo "Syncing gafaelfawr..."
  argocd app sync gafaelfawr \
    --port-forward \
    --port-forward-namespace argocd
fi

echo "Syncing remaining applications..."
argocd app sync -l "argocd.argoproj.io/instance=science-platform" \
  --port-forward \
  --port-forward-namespace argocd

echo ''
echo "You can now check on your argo cd installation by running:"
echo "kubectl port-forward service/argocd-server -n argocd 8080:443"
echo "For the ArgoCD admin password:"
echo "vault kv get --field=admin.plaintext_password $VAULT_PATH_PREFIX/argocd"
