#!/bin/bash -xe
USAGE="Usage: ./install.sh ENVIRONMENT VAULT_ROLE_ID_PATH VAULT_SECRET_ID"
ENVIRONMENT=${1:?$USAGE}
#export VAULT_TOKEN=${2:?$USAGE}
export VAULT_ROLE_ID_PATH=${2:?$USAGE}
echo "VAULT_ROLE_ID_PATH=${VAULT_ROLE_ID_PATH}"
export VAULT_SECRET_ID=${3:?$USAGE}
echo "VAULT_SECRET_ID=${VAULT_SECRET_ID}"
export VAULT_ADDR=${VAULT_ADDR:-https://vault.lsst.codes}
#VAULT_PATH_PREFIX=`yq -r .vault_path_prefix ../science-platform/values-$ENVIRONMENT.yaml`
VAULT_PATH_PREFIX=$(cat ../science-platform/values-$ENVIRONMENT.yaml | grep vault_path_prefix | awk '{print $2}')
ARGOCD_PASSWORD=`vault kv get --field=argocd.admin.plaintext_password $VAULT_PATH_PREFIX/installer`

GIT_URL=`git config --get remote.origin.url`
HTTP_URL=$( echo "$GIT_URL" | sed s%git@%https://% | sed s%github.com:%github.com/% ).git
# Github runs in a detached head state, but sets GITHUB_REF,
# extract the branch from it.  If we're there, use that branch.
# git branch --show-current will return empty in deatached head.
GIT_BRANCH=${GITHUB_HEAD_REF:-`git rev-parse --abbrev-ref HEAD`}

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
  --from-literal=VAULT_ROLE_ID=$(vault read --format=json ${VAULT_ROLE_ID_PATH}/role-id | jq -M .data.role_id  | sed 's/"//g') \
  --from-literal=VAULT_SECRET_ID=${VAULT_SECRET_ID} \
  --from-literal=VAULT_TOKEN_MAX_TTL=600 \
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
  --values ../services/vault-secrets-operator/values.yaml \
  --values ../services/vault-secrets-operator/values-$ENVIRONMENT.yaml \
  --create-namespace \
  --namespace vault-secrets-operator \
  --timeout 15m \
  --wait

echo "Update / install argocd using helm..."
helm dependency update ../services/argocd
helm upgrade argocd ../services/argocd \
  --install \
  --values ../services/argocd/values.yaml \
  --values ../services/argocd/values-$ENVIRONMENT.yaml \
  --set global.vaultSecretsPath="$VAULT_PATH_PREFIX" \
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
  --repo $HTTP_URL \
  --path science-platform --dest-namespace default \
  --dest-server https://kubernetes.default.svc \
  --upsert \
  --revision $GIT_BRANCH \
  --port-forward \
  --port-forward-namespace argocd \
  --helm-set repoURL=$HTTP_URL \
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
    --plaintext \
    --port-forward \
    --port-forward-namespace argocd
fi

# Wait for the cert-manager's webhook to finish deploying by running
# kubectl, argocd's sync doesn't seem to wait for this to finish.
if [ $(yq -r .cert_manager.enabled ../science-platform/values-$ENVIRONMENT.yaml) == "true" ];
then
  echo "Syncing cert-manager..."
  argocd app sync cert-manager \
    --plaintext \
    --port-forward \
    --port-forward-namespace argocd && \
    kubectl -n cert-manager rollout status deploy/cert-manager-webhook
fi

if [ $(yq -r .postgres.enabled ../science-platform/values-$ENVIRONMENT.yaml) == "true" ];
then
  echo "Syncing postgres..."
  argocd app sync postgres \
    --plaintext \
    --port-forward \
    --port-forward-namespace argocd
fi

if [ $(yq -r .gafaelfawr.enabled ../science-platform/values-$ENVIRONMENT.yaml) == "true" ];
then
  echo "Syncing gafaelfawr..."
  argocd app sync gafaelfawr \
    --plaintext \
    --port-forward \
    --port-forward-namespace argocd
fi

echo "Sync remaining science platform apps"
argocd app sync -l "argocd.argoproj.io/instance=science-platform" \
  --plaintext \
  --port-forward \
  --port-forward-namespace argocd

echo "You can now check on your argo cd installation by running:"
echo "kubectl port-forward service/argocd-server -n argocd 8080:443"
echo "For the ArgoCD admin password:"
echo "vault kv get --field=argocd.admin.plaintext_password $VAULT_PATH_PREFIX/installer"
