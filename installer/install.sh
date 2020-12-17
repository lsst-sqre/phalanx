#!/bin/bash -ex
USAGE="Usage: ./install.sh ENVIRONMENT VAULT_TOKEN"
ENVIRONMENT=${1:?$USAGE}
VAULT_TOKEN=${2:?$USAGE}
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
  --dry-run -o yaml | kubectl apply -f -

echo "Update / install vault-secrets-operator..."
# ArgoCD depends on pull-secret, which depends on vault-secrets-operator.
helm dependency build ../services/vault-secrets-operator
helm upgrade vault-secrets-operator ../services/vault-secrets-operator \
  --install \
  --values ../services/vault-secrets-operator/values-$ENVIRONMENT.yaml \
  --create-namespace \
  --namespace vault-secrets-operator \
  --timeout 15m \
  --wait

echo "Update / install argocd using helm3..."
helm dependency build ../services/argocd
helm upgrade argocd ../services/argocd \
  --install \
  --values ../services/argocd/values-$ENVIRONMENT.yaml \
  --create-namespace \
  --namespace argocd \
  --timeout 15m \
  --wait

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
argocd app sync cert-manager \
  --port-forward \
  --port-forward-namespace argocd
# Wait for the cert-manager's webhook to finish deploying by running
# kubectl.  argocd's sync doesn't seem to wait for this to finish.
kubectl -n cert-manager rollout status deploy/cert-manager-webhook

argocd app sync cert-issuer \
  --port-forward \
  --port-forward-namespace argocd

echo "Sync remaining science platform apps"
argocd app sync -l "argocd.argoproj.io/instance=science-platform" \
  --port-forward \
  --port-forward-namespace argocd

echo "You can now check on your argo cd installation by running:"
echo "kubectl port-forward service/argocd-server -n argocd 8080:443"
echo "Login with username: admin password: $ARGOCD_PASSWORD"
