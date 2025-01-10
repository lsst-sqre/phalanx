helm template . \
    --name-template ppdb-replication --namespace ppdb-replication \
    --kube-version 1.27 --set global.host=usdf-rsp-dev.slac.stanford.edu \
    --set global.baseUrl=https://usdf-rsp-dev.slac.stanford.edu \
    --set global.vaultSecretsPath=secret/rubin/usdf-rsp-dev \
    --values ./values.yaml --values ./values-usdfdev.yaml &> helm_template.yaml
