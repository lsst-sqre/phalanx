#!/bin/bash -e

################################################################################
# install.sh - Install script for the Rubin Science Platform
################################################################################

# Usage:
#   ./install.sh ENVIRONMENT=env [VAULT_ROLE_ID=<vault> VAULT_SECRET_ID=<vault> | VAULT_TOKEN=<value> [VAULT_TOKEN_LEASE_DURATION=<value>]]

# Arguments
#   - The environment variable is mandatory and should be provided as the first argument.
#   - If two positional arguments are provided, assume they are VAULT_ROLE_ID and VAULT_SECRET_ID.
#   - If named arguments are provided, parse them for ENVIRONMENT, VAULT_ROLE_ID, VAULT_SECRET_ID, VAULT_TOKEN, and VAULT_TOKEN_LEASE_DURATION.

# Environment Configuration:
#   The environment configuration is retrieved from ../environments/values-${ENVIRONMENT}.yaml.

# Usage Examples:
#   Using authentication with an approle:
#     ./install.sh ENVIRONMENT=myenv VAULT_ROLE_ID=your-vault-id VAULT_SECRET_ID=your-secret
#     ./install.sh myenv your-vault-id your-secret # Uses VAULT_ROLE_ID and VAULT_SECRET_ID
#
#   Using authentication with a token:
#     ./install.sh ENVIRONMENT=myenv VAULT_TOKEN=your-vault-token
#     ./install.sh ENVIRONMENT=myenv VAULT_TOKEN=your-vault-token VAULT_TOKEN_LEASE_DURATION=31536000
#     ./install.sh myenv VAULT_TOKEN=your-vault-token

# Script Dependencies:
#   - yq: Used for parsing YAML files.
#   - vault: Used for interacting with HashiCorp Vault.
#   - kubectl: Kubernetes command-line tool.
#   - helm: Kubernetes package manager.

# Notes:
#   - The script assumes that the specified environment exists, and is available under ../environments/ and has the required charts under ../applications/
#   - It creates or updates Argo CD and Vault secrets based on the provided credentials.

# Exit codes:
#   - 0: Success
#   - 1: Error

################################################################################

USAGE="Usage: ./install.sh ENVIRONMENT=env [VAULT_ROLE_ID=<vault> VAULT_SECRET_ID=<vault> | VAULT_TOKEN=<value> [VAULT_TOKEN_LEASE_DURATION=<value>]]"

unset ENVIRONMENT
unset VAULT_ROLE_ID
unset VAULT_TOKEN
unset VAULT_TOKEN_LEASE_DURATION
unset VAULT_SECRET_ID

# Function to display usage and exit
display_usage() {
    echo "$USAGE"
    exit 1
}

# Function to create Kubernetes secret
create_kubernetes_secret() {
    local namespace="$1"
    shift
    kubectl create secret generic vault-credentials \
      --namespace "$namespace" \
      --dry-run=client -o yaml "$@" | kubectl apply -f -
}

# Function to check for dependencies
check_dependencies() {
    local dependencies=("yq" "vault" "kubectl" "helm")

    for cmd in "${dependencies[@]}"; do
        if ! command -v "$cmd" > /dev/null 2>&1; then
            echo "Error: $cmd not found. Please install $cmd and try again."
            exit 1
        fi
    done
}

# Check that the dependencies are installed
check_dependencies

# Extract environment
if [[ $1 == ENVIRONMENT=* ]]; then
    ENVIRONMENT="${1#*=}"
    shift
elif [[ $1 =~ ^[a-zA-Z0-9_-]+$ ]]; then
    ENVIRONMENT="$1"
    shift
else
    display_usage
fi

# Extract named arguments
for arg in "$@"; do
    case "$arg" in
        environment=*)
            ENVIRONMENT="${arg#*=}"
            ;;
        VAULT_ROLE_ID=*|vault_role_id=*)
            VAULT_ROLE_ID="${arg#*=}"
            ;;
        VAULT_SECRET_ID=*|vault_secret_id=*)
            VAULT_SECRET_ID="${arg#*=}"
            ;;
        VAULT_TOKEN=*|vault_token=*)
            VAULT_TOKEN="${arg#*=}"
            ;;
        VAULT_TOKEN_LEASE_DURATION=*|vault_token_lease_duration=*)
            VAULT_TOKEN_LEASE_DURATION="${arg#*=}"
            ;;
        *)
            ;;
    esac
done


# If VAULT_ROLE_ID and VAULT_SECRET_ID are not set from named arguments, check positional arguments
if [ -z "$VAULT_ROLE_ID" ] || [ -z "$VAULT_SECRET_ID" ]; then
    # If two positional arguments are provided, assume they are VAULT_ROLE_ID and VAULT_SECRET_ID
    if [ $# -ge 2 ]; then
        VAULT_ROLE_ID=$1
        VAULT_SECRET_ID=$2
        shift 2
    fi
fi

# Get environment configuration
config="../environments/values-${ENVIRONMENT}.yaml"

echo "Getting Git branch and remote information..."
GIT_URL=$(git config --get remote.origin.url)
# Github runs in a detached head state, but sets GITHUB_REF,
# extract the branch from it.  If we're there, use that branch.
# git branch --show-current will return empty in deatached head.
GIT_BRANCH=${GITHUB_HEAD_REF:-$(git branch --show-current)}

echo "Logging on to Vault..."

VAULT_ADDR=""
if grep '^vaultUrl:' "$config" >/dev/null; then
    VAULT_ADDR=$(yq -r .vaultUrl "$config")
else
    VAULT_ADDR=$(yq -r .vaultUrl ../environments/values.yaml)
fi

export VAULT_ADDR=$VAULT_ADDR

# Check if VAULT_ROLE_ID and VAULT_SECRET_ID are provided, if so generate VAULT_TOKEN
if [ -n "$VAULT_ROLE_ID" ] && [ -n "$VAULT_SECRET_ID" ]; then
    # If VAULT_TOKEN is not provided, generate it using VAULT_ROLE_ID and VAULT_SECRET_ID
    if [ -z "$VAULT_TOKEN" ]; then
        VAULT_TOKEN=$(vault write auth/approle/login role_id="$VAULT_ROLE_ID" secret_id="$VAULT_SECRET_ID" | grep 'token ' | awk '{ print $2 }')
    fi
fi

# Check if VAULT_ROLE_ID and VAULT_SECRET_ID are not provided, but VAULT_TOKEN is
if [ -z "$VAULT_ROLE_ID" ] || [ -z "$VAULT_SECRET_ID" ]; then
    # Check if VAULT_TOKEN is provided
    if [ -z "$VAULT_TOKEN" ]; then
        echo "Invalid arguments provided. Please provide either VAULT_ROLE_ID and VAULT_SECRET_ID or VAULT_TOKEN."
        display_usage
    else
        if [ -z "$VAULT_TOKEN_LEASE_DURATION" ]; then
          VAULT_TOKEN_LEASE_DURATION=31536000  # Default lease duration: 1 year
        fi
    fi
fi

export VAULT_TOKEN=$VAULT_TOKEN

VAULT_PATH_PREFIX=$(yq -r .vaultPathPrefix "$config")
ARGOCD_PASSWORD=$(vault kv get --field=admin.plaintext_password "$VAULT_PATH_PREFIX"/argocd)

echo "Putting Vault credentials in a secret for vault-secrets-operator..."
# The namespace may not exist already, but don't error if it does.
kubectl create ns vault-secrets-operator || true

# Create Kubernetes secret based on authentication method
if [ -n "$VAULT_ROLE_ID" ] && [ -n "$VAULT_SECRET_ID" ]; then
    create_kubernetes_secret "vault-secrets-operator" \
        --from-literal=VAULT_ROLE_ID="$VAULT_ROLE_ID" \
        --from-literal=VAULT_SECRET_ID="$VAULT_SECRET_ID"
elif [ -n "$VAULT_TOKEN" ]; then
    create_kubernetes_secret "vault-secrets-operator" \
        --from-literal=VAULT_TOKEN="$VAULT_TOKEN" \
        --from-literal=VAULT_TOKEN_LEASE_DURATION="$VAULT_TOKEN_LEASE_DURATION"
else
    echo "Invalid arguments provided. Please provide either VAULT_ROLE_ID and VAULT_SECRET_ID or VAULT_TOKEN."
    display_usage
fi

# Argo CD depends a Vault-created secret for its credentials, so
# vault-secrets-operator has to be installed first.
echo "Updating or installing vault-secrets-operator..."
helm dependency update ../applications/vault-secrets-operator
helm upgrade vault-secrets-operator ../applications/vault-secrets-operator \
  --install \
  --values ../applications/vault-secrets-operator/values.yaml \
  --values "../applications/vault-secrets-operator/values-$ENVIRONMENT.yaml" \
  --set "vault-secrets-operator.vault.address=$VAULT_ADDR" \
  --create-namespace \
  --namespace vault-secrets-operator \
  --timeout 5m \
  --wait

echo "Updating or installing Argo CD using Helm..."
helm dependency update ../applications/argocd
helm upgrade argocd ../applications/argocd \
  --install \
  --values ../applications/argocd/values.yaml \
  --values "../applications/argocd/values-$ENVIRONMENT.yaml" \
  --set "global.vaultSecretsPath=$VAULT_PATH_PREFIX" \
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
  --password "$ARGOCD_PASSWORD"

echo "Creating the top-level Argo CD application..."
argocd app create science-platform \
  --repo "$GIT_URL" \
  --path environments --dest-namespace default \
  --dest-server https://kubernetes.default.svc \
  --upsert \
  --revision "$GIT_BRANCH" \
  --port-forward \
  --port-forward-namespace argocd \
  --helm-set "repoUrl=$GIT_URL" \
  --helm-set "targetRevision=$GIT_BRANCH" \
  --values values.yaml \
  --values "values-$ENVIRONMENT.yaml"

echo "Syncing the top-level Argo CD application..."
argocd app sync science-platform \
  --port-forward \
  --port-forward-namespace argocd \
  --timeout 30

echo "Moving the top-level Argo CD application into infrastructure..."
argocd app set science-platform --project infrastructure \
  --port-forward \
  --port-forward-namespace argocd

echo "Syncing Argo CD..."
timeout 30 argocd app sync argocd \
  --port-forward \
  --port-forward-namespace argocd \
  --timeout 30 || \
argocd login \
  --plaintext \
  --port-forward \
  --port-forward-namespace argocd \
  --username admin \
  --password "$ARGOCD_PASSWORD" && \
timeout 30 argocd app sync argocd \
  --port-forward \
  --port-forward-namespace argocd \
  --timeout 30

echo "Waiting for Argo CD to finish syncing..."
kubectl -n argocd rollout status deployment/argocd-server
kubectl -n argocd rollout status deployment/argocd-repo-server
kubectl -n argocd rollout status statefulset/argocd-application-controller

echo "Logging in to Argo CD..."
argocd login \
  --plaintext \
  --port-forward \
  --port-forward-namespace argocd \
  --username admin \
  --password "$ARGOCD_PASSWORD"

if [ "$(yq -r '.applications."ingress-nginx"' "$config")" != "false" ]; then
  echo "Syncing ingress-nginx..."
  argocd app sync ingress-nginx \
    --port-forward \
    --port-forward-namespace argocd
fi

if [ "$(yq -r '.applications."cert-manager"' "$config")" != "false" ]; then
  echo "Syncing cert-manager..."
  argocd app sync cert-manager \
    --port-forward \
    --port-forward-namespace argocd && \

  # Wait for the cert-manager's webhook to finish deploying by running
  # kubectl, argocd's sync doesn't seem to wait for this to finish.
  kubectl -n cert-manager rollout status deployment/cert-manager-webhook
fi

if [ "$(yq -r .applications.postgres "$config")" == "true" ]; then
  echo "Syncing postgres..."
  argocd app sync postgres \
    --port-forward \
    --port-forward-namespace argocd
fi

if [ "$(yq -r .applications.gafaelfawr "$config")" != "false" ]; then
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
echo "You can now check on your Argo CD installation by running:"
echo "kubectl port-forward service/argocd-server -n argocd 8080:443"
echo "For the ArgoCD admin password:"
echo "vault kv get --field=admin.plaintext_password $VAULT_PATH_PREFIX/argocd"
