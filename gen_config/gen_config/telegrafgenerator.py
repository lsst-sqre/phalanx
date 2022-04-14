import yaml

from .phalanxconfiggenerator import PhalanxConfigGenerator
from .prometheus import prometheus_config

from typing import Any, Dict

class TelegrafGenerator(PhalanxConfigGenerator):
    """
    TelegrafGenerator generates configuration files for the telegraf
    application.
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.output_path = self.phalanx_root + "/services/telegraf"

    def build_config(self) -> None:
        self.config["generic"] = self.build_generic_yaml()
        for instance in self.instances:
            self.config[instance]=self.build_instance_yaml(instance)

    def build_generic_yaml(self) -> None:
        obj = {
            "telegraf": {
                # -- Allow network access to JupyterHub pod.                
                "podLabels": {
                    "hub.jupyter.org/network-access-hub": "true",
                },
                "env": [
                    {
                        # -- Token to communicate with InfluxDB_v2
                        "name": "INFLUX_TOKEN",
                        "valueFrom": {
                            "secretKeyRef": {
                                "name": "telegraf",
                                "key": "influx-token",
                            },
                        },
                    },
                ],
                "service": {
                    # -- Telegraf service.                    
                    "enabled": False,
                },
                "config": {
                    "agent": {
                        "omit_hostname": True,
                    },
                    "global_tags": {
                        # -- Cluster name -- should be FQDN of RSP endpoint
                        # @default -- None: must be set
                        "cluster": "",
                    },
                },
                "tplVersion": 2,
            },
            # -- Path to the Vault secrets
            # -- (`secret/k8s_operator/<hostname>`)
            # @default -- None: must be set
            "vaultSecretsPath": "",
        }
        return yaml.dump(obj)

    def build_instance_yaml(self, instance:str) -> str:
        inst_obj =  self.instances.get(instance, {})
        if not inst_obj:
            return ""
        # If telegraf isn't enabled for the site, don't write anything.
        if not inst_obj.get("telegraf", {}).get("enabled", ""):
            return ""
        secrets_path=inst_obj.get("vault_path_prefix","")
        cluster = inst_obj.get("fqdn","")
        obj = { "vaultSecretsPath": secrets_path,
                "telegraf": {
                    "config": {
                        "global_tags": {
                            "cluster": cluster,
                        },
                        "outputs": [],
                        "inputs": [],
                    },
                },
               }
        for app in prometheus_config:
            if not inst_obj.get(app.replace('-','_'),
                                {}).get("enabled",False):
                continue
            # The app is enabled, so we should monitor it.
            for service in prometheus_config[app]:
                # Construct the outputs (bucket-separated)
                out_obj = self.make_output_object(app, service)
                obj["telegraf"]["config"]["outputs"].append(out_obj)
                # Construct the inputs (Prometheus metric endpoints)
                inp_obj = self.make_input_object(app, service)
                obj["telegraf"]["config"]["inputs"].append(inp_obj)
        return yaml.dump(obj)
                
            
    def make_input_object(self, app: str, service: str) -> Dict[str, Any]:
        obj={
            "prometheus": {
                "urls": [
                    prometheus_config[app][service],
                ],
                "tags": {
                    "prometheus_app": app.replace("-","_"),
                },
                "name_override": f"prometheus_{service}",
                "metric_version": 2,
            },
        }
        return obj

    def make_output_object(self, app: str, service: str) -> Dict[str, Any]:
        obj = {
            "influxdb_v2": {
                "urls": [
                    "https://monitoring.lsst.codes",
                ],
                "bucket": app.replace("-","_"),
                "token": "$INFLUX_TOKEN",
                "organization": "square",
                "tagpass": {
                    "prometheus_app": [
                        app.replace("-","_"),
                    ],
                },
            },
        }
        return obj
