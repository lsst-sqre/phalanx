from .phalanxconfiggenerator import PhalanxConfigGenerator

class TelegrafDSGenerator(PhalanxConfigGenerator):
    """
    TelegrafDSGenerator generates configuration files for the telegraf-ds
    application.
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.output_path = self.phalanx_root + "/services/telegraf-ds"

    def build_config(self) -> None:
        self.config["generic"] = self.build_generic_yaml()
        for instance in self.instances:
            self.config[instance]=self.build_instance_yaml(instance)

    def build_generic_yaml(self) -> None:
        cf='''# -- Path to the Vault secrets (`secret/k8s_operator/<hostname>/telegraf`)
# shared with telegraf (non-DaemonSet)
# @default -- None, must be set
vaultSecretsPath: ""
telegraf-ds:
  env:
    # -- Token to communicate with Influx
    - name: INFLUX_TOKEN
      valueFrom:
        secretKeyRef:
          name: telegraf
          key: influx-token
'''
        cf += self.build_telegraf_override_conf("generic")
        return cf

    def build_instance_yaml(self, instance:str) -> str:
        inst_obj = self.instances.get(instance, {})
        if not inst_obj.get("telegraf-ds",{}).get("enabled",""):
            return ""
        secrets_path=self.instances[instance].get("vault_path_prefix","")
        cf = f"vaultSecretsPath: \"{secrets_path}\"\n"
        cf += "telegraf-ds:\n"
        cf += self.build_telegraf_override_conf(instance)
        return cf
            
    def build_telegraf_override_conf(self, instance: str) -> str:
        """For each instance, generate the (literal) contents for
        telegraf.conf"""
        endpoint=self.instances.get(instance,{}).get("fqdn","no_endpoint")
        tc  =   "  override_config:\n"
        tc +=   "    toml: |+\n"
        tc +=   "      [global_tags]\n"
        tc +=  f"        cluster = \"{endpoint}\"\n"
        tc += """      [agent]
        hostname = "telegraf-$HOSTIP"
      [[inputs.kubernetes]]
        url = "https://$HOSTIP:10250"
        bearer_token = "/var/run/secrets/kubernetes.io/serviceaccount/token"
        insecure_skip_verify = true
        namepass = ["kubernetes_pod_container"]
        fieldpass = ["cpu_usage_nanocores", "memory_usage_bytes"]
"""
        tc += self.build_outputs(instance)
        return tc

    def build_outputs(self, instance: str) -> str:
        """For each instance, generate the list of outputs, one for each
        enabled service.
        """
        outp = ""
        i_obj = self.instances.get(instance, {})
        for app in self.applications:
            if not i_obj.get(app,{}).get("enabled",False):
                continue
            namespace_set = self.namespaces.get(app, None)
            if not namespace_set:
                continue
            for namespace in namespace_set:
                outp +='''      [[outputs.influxdb_v2]]
        urls = ["https://monitoring.lsst.codes"]
        token = "$INFLUX_TOKEN"
        organization = "square"
'''
                bucket = namespace.replace("-", "_")
                outp += f"        bucket = \"{bucket}\"\n"
                outp += "        [outputs.influxdb_v2.tagpass]\n"
                outp += f"          namespace = [\"{namespace}\"]\n"
        return outp
