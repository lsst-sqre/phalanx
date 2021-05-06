#!/bin/bash -xe
USAGE="Usage: ./install.sh ENVIRONMENT VAULT_TOKEN"
ENVIRONMENT=${1:?$USAGE}
#export VAULT_TOKEN=${2:?$USAGE}
export VAULT_ADDR=${VAULT_ADDR:-https://vault.lsst.codes}
#VAULT_PATH_PREFIX=`yq -r .vault_path_prefix ../science-platform/values-$ENVIRONMENT.yaml`
VAULT_PATH_PREFIX=$(cat ../science-platform/values-usdfdev.yaml | grep vault_path_prefix | awk '{print $2}')
ARGOCD_PASSWORD=`vault kv get --field=argocd.admin.plaintext_password $VAULT_PATH_PREFIX/installer`

GIT_URL=`git config --get remote.origin.url`
# Github runs in a detached head state, but sets GITHUB_REF,
# extract the branch from it.  If we're there, use that branch.
# git branch --show-current will return empty in deatached head.
GIT_BRANCH=${GITHUB_HEAD_REF:-`git branch --show-current`}

echo "Set VAULT_TOKEN in a secret for vault-secrets-operator..."
# The namespace may not exist already, but don't error if it does.
kubectl create ns vault-secrets-operator || true
#kubectl create secret generic vault-secrets-operator \
#  --namespace vault-secrets-operator \
#  --from-literal=VAULT_TOKEN=$VAULT_TOKEN \
#  --from-literal=VAULT_TOKEN_LEASE_DURATION=31536000 \
#  --dry-run -o yaml | kubectl apply -f -
kubectl create secret generic vault-secrets-operator \
  --namespace vault-secrets-operator \
  --from-literal=VAULT_ROLE_ID=$(vault read --format=json auth/approle/role/rubin-data-dev.slac.stanford.edu/role-id | jq -M .data.role_id  | sed 's/"//g') \
  --from-literal=VAULT_SECRET_ID=$(vault write -f --format=json auth/approle/role/rubin-data-dev.slac.stanford.edu/secret-id | jq .data.secret_id | sed 's/"//g') \
  --from-literal=VAULT_TOKEN_MAX_TTL=600 \
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
argocd app sync ingress-nginx \
  --port-forward \
  --port-forward-namespace argocd

# Wait for the cert-manager's webhook to finish deploying by running
# kubectl.  argocd's sync doesn't seem to wait for this to finish.
# This is a little tricky on the bash.  If cert-manager isn't used,
# the argocd command will fail, then we will continue.  If it doesn't
# fail, wait for it to finish.
(argocd app sync cert-manager \
  --port-forward \
  --port-forward-namespace argocd && \
kubectl -n cert-manager rollout status deploy/cert-manager-webhook) || true

# Sync cert-issuer, but don't exit if this environment doesn't use it.
argocd app sync cert-issuer \
  --port-forward \
  --port-forward-namespace argocd || true

echo "Sync remaining science platform apps"
argocd app sync -l "argocd.argoproj.io/instance=science-platform" \
  --port-forward \
  --port-forward-namespace argocd

echo "You can now check on your argo cd installation by running:"
echo "kubectl port-forward service/argocd-server -n argocd 8080:443"
echo "For the ArgoCD admin password:"
echo "vault kv get --field=argocd.admin.plaintext_password $VAULT_PATH_PREFIX/installer"
