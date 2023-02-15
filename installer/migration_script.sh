#!/bin/bash -xe

ENVIRONMENT="usdfdev"
GIT_URL="https://github.com/lsst-sqre/phalanx.git"
GIT_BRANCH=${GITHUB_HEAD_REF:-`git rev-parse --abbrev-ref HEAD`}
VAULT_PATH_PREFIX="secret/rubin/usdf-rsp-dev"
ARGOCD_PASSWORD=`vault kv get --field=argocd.admin.plaintext_password $VAULT_PATH_PREFIX/installer`

argocd login \
  --plaintext \
  --port-forward \
  --port-forward-namespace argocd \
  --username admin \
  --password $ARGOCD_PASSWORD

argocd app create science-platform \
  --repo $GIT_URL \
  --path environments --dest-namespace default \
  --dest-server https://kubernetes.default.svc \
  --upsert \
  --revision $GIT_BRANCH \
  --port-forward \
  --port-forward-namespace argocd \
  --helm-set repoURL=$GIT_URL \
  --helm-set targetRevision=$GIT_BRANCH \
  --values values-$ENVIRONMENT.yaml

argocd app sync science-platform \
  --port-forward \
  --port-forward-namespace argocd

