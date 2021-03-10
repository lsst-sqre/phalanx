#!/usr/bin/env python3
import argparse
from base64 import b64encode
import bcrypt
from collections import defaultdict
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import secrets
import yaml


class SecretGenerator:
    def __init__(self, regenerate):
        self.secrets = {}
        self.regenerate = regenerate

    def generate(self):
        self._pull_secret()
        self._postgres()
        self._log()
        self._tap()
        self._nublado()
        self._nublado2()
        self._mobu()
        self._gafaelfawr()
        self._argocd()
        self._portal()

        self.input_field("cert-manager", "enabled", "Use cert-manager? (y/n):")
        use_cert_manager = self.secrets["cert-manager"]["enabled"]
        if use_cert_manager == "y":
            self._cert_manager()
        elif use_cert_manager == "n":
            self._ingress_nginx()
        else:
            raise Exception("Invalid cert manager enabled")

    def load(self):
        for f in Path('secrets').iterdir():
            print(f"Loading {f}")
            component = os.path.basename(f)
            self.secrets[component] = json.loads(f.read_text())

    def save(self):
        os.makedirs("secrets", exist_ok=True)

        for k, v in self.secrets.items():
            with open(f"secrets/{k}", "w") as f:
                f.write(json.dumps(v))

    def input_field(self, component, name, description):
        default = self.secrets[component].get(name, "")
        prompt_string = f"[{component} {name}] ({description}): [current: {default}] "
        input_string = input(prompt_string)

        if input_string:
            self.secrets[component][name] = input_string


    def input_file(self, component, name, description):
        current = self.secrets.get(component, {}).get(name, "")
        print(f"[{component} {name}] ({description})")
        print(f"Current contents:\n{current}")
        prompt_string = f"New filename with contents (empty to not change): "
        fname = input(prompt_string)

        if fname:
            with open(fname, "r") as f:
                self.secrets[component][name] = f.read()


    def _set_generated(self, component, name, new_value):
        if self.regenerate:
            self.secrets[component][name] = new_value

    def _tap(self):
        self.input_field("tap", "slack_webhook_url", "slack webhook url for querymonkey")
        self.input_file("tap", "google_creds.json", "file containing google service account credentials")

    def _log(self):
        def gen_pw_and_hash():
            pw = secrets.token_hex(16)
            h = bcrypt.hashpw(
                pw.encode("ascii"), bcrypt.gensalt(rounds=15)
            ).decode("ascii")
            return (pw, h)

        admin = gen_pw_and_hash()
        kibana = gen_pw_and_hash()
        logstash = gen_pw_and_hash()

        internal_users = {
            "_meta": {
                "type": "internalusers",
                "config_version": 2,
            },
            "admin": {
                "hash": admin[1],
                "reserved": True,
                "backend_roles": ["admin"],
                "description": "Admin user",
            },
            "kibana": {
                "hash": kibana[1],
                "backend_roles": ["kibanauser"],
                "description": "Kibana user",
            },
            "logstash": {
                "hash": logstash[1],
                "reserved": False,
                "backend_roles": ["logstash"],
                "description": "Logstash writing user",
            },
        }

        # username / password / cookie is the elasticsearch admin user,
        # and this key is unfortunately hardcoded by the chart.
        # fluentd and kibana passwords are also passed through, but these
        # are tied to the hashes that are present in the internal_users
        # yaml file, where the bcrypt'd password is stored.
        self._set_generated("log", "username", "admin")
        self._set_generated("log", "password", admin[0])
        self._set_generated("log", "cookie", secrets.token_urlsafe(32))
        self._set_generated("log", "internal_users.yml", yaml.dump(internal_users))
        self._set_generated("log", "logstash-password", logstash[0])
        self._set_generated("log", "kibana-password", kibana[0])


    def _postgres(self):
        self._set_generated("postgres", "exposurelog_password", secrets.token_hex(32))
        self._set_generated("postgres", "jupyterhub_password", secrets.token_hex(32))
        self._set_generated("postgres", "root_password", secrets.token_hex(64))


    def _nublado2(self):
        crypto_key = ";".join([secrets.token_hex(32), secrets.token_hex(32)])
        self._set_generated("nublado2", "crypto_key", crypto_key)
        self._set_generated("nublado2", "proxy_token", secrets.token_hex(32))


    def _nublado(self):
        crypto_key = ";".join([secrets.token_hex(32), secrets.token_hex(32)])
        self._set_generated("nublado", "jupyterhub_crypto_key", crypto_key)
        self._set_generated("nublado", "configproxy_auth_token", secrets.token_hex(32))

        # Pluck the password out of the postgres portion to generate our connect string.
        db_pass = self.secrets["postgres"]["jupyterhub_password"]
        session_db_url = f"postgres://jovyan:{db_pass}@postgres.postgres/jupyterhub"
        self.secrets["nublado"]["session_db_url"] = session_db_url


    def _mobu(self):
        self.input_field("mobu", "ALERT_HOOK", "Slack webhook for reporting mobu alerts.  Or use None for no alerting.")


    def _cert_manager(self):
        self.input_field("cert-manager", "aws-secret-access-key", "AWS secret access key for zone for DNS cert solver.")


    def _gafaelfawr(self):
        key = rsa.generate_private_key(
            backend=default_backend(), public_exponent=65537, key_size=2048
        )

        key_bytes = key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        )

        self._set_generated("gafaelfawr", "redis-password", os.urandom(32).hex())
        self._set_generated("gafaelfawr", "session-secret", Fernet.generate_key().decode())
        self._set_generated("gafaelfawr", "signing-key", key_bytes.decode())

        self.input_field("gafaelfawr", "auth_type", "Use cilogon or github?")
        auth_type = self.secrets["gafaelfawr"]["auth_type"]
        if auth_type == "cilogon":
            self.input_field("gafaelfawr", "cilogon-client-secret", "CILogon client secret")
        elif auth_type == "github":
            self.input_field("gafaelfawr", "github-client-secret", "GitHub client secret")
        else:
            raise Exception("Invalid auth provider")


    def _pull_secret(self):
        self.input_file("pull-secret", ".dockerconfigjson", ".docker/config.json to pull images")


    def _ingress_nginx(self):
        self.input_file("ingress-nginx", "tls.key", "Certificate private key")
        self.input_file("ingress-nginx", "tls.crt", "Certificate chain")


    def _argocd(self):
        self.input_field("installer", "argocd.admin.plaintext_password", "Admin password for ArgoCD?")
        pw = self.secrets["installer"]["argocd.admin.plaintext_password"]
        h = bcrypt.hashpw(
            pw.encode("ascii"), bcrypt.gensalt(rounds=15)
        ).decode("ascii")
        now_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        self._set_generated("argocd", "admin.password", h)
        self._set_generated("argocd", "admin.passwordMtime", now_time)
        self._set_generated("argocd", "server.secretkey", secrets.token_hex(16))


    def _portal(self):
        pw = secrets.token_hex(32)
        self._set_generated("portal", "ADMIN_PASSWORD", pw)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="generate_secrets")
    parser.add_argument('--regenerate', default=False, action='store_true')
    args = parser.parse_args()

    sg = SecretGenerator(args.regenerate)
    sg.load()
    sg.generate()
    sg.save()
