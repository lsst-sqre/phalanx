#!/usr/bin/env python3

# Run this with one argument: the cluster name that you want tagged in
# the database (e.g. "data-dev.lsst.cloud").  It will generate the
# override_config.toml field for the appropriate configuration, on stdout.

import sys

try:
    c=sys.argv[1]
except:
    c=""

print( "  override_config:")
print( "    toml: |+")
print( "      [ global_tags ]")
print(f"        cluster = \"{c}\"")
print(
"""      [ agent ]
        hostname = "telegraf-$HOSTIP"
      [[inputs.kubernetes]]
        url = "https://$HOSTIP:10250"
        bearer_token = "/var/run/secrets/kubernetes.io/serviceaccount/token"
        insecure_skip_verify = true
        namepass = ["kubernetes_pod_container"]
        fieldpass = ["cpu_usage_nanocores", "memory_usage_bytes"]""")

namespaces = ("argocd",
              "cachemachine",
              "cert-manager",
              "datalinker",
              "gafaelfawr",
              "ingress-nginx",
              "mobu",
              "moneypenny",
              "noteburst",
              "nublado2",
              "obstap",
              "portal",
              "postgres",
              "sasquatch",
              "semaphore",
              "sherlock",
              "squareone",
              "strimzi",
              "tap",
              "tap-schema",
              "telegraf",
              "telegraf-ds",
              "times-square",
              "vault-secrets-operator")

for n in namespaces:
    print(
        '''      [[outputs.influxdb_v2]]
        urls = ["https://monitoring.lsst.codes"]
        token = "$INFLUX_TOKEN"
        organization = "square"''')
    b=n.replace("-","_")
    print(f"        bucket = \"k8s_{b}\"")
    print( "        [outputs.influxdb_v2.tagpass]")
    print(f"          namespace = [\"{n}\"]")
    
