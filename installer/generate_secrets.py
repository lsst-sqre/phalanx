#!/usr/bin/env python3
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


def input_field(s, component, name, description):
    default = s[component].get(name, "")
    prompt_string = f"[{component} {name}] ({description}): [current: {default}] "
    input_string = input(prompt_string)

    if input_string:
        s[component][name] = input_string


def input_file(s, component, name, description):
    current = s.get(component, {}).get(name, "")
    print(f"[{component} {name}] ({description})")
    print(f"Current contents:\n{current}")
    prompt_string = f"New filename with contents (empty to not change): "
    fname = input(prompt_string)

    if fname:
        with open(fname, "r") as f:
            s[component][name] = f.read()


def set_generated_secret(s, component, name, new_value):
    regenerate = True
    if regenerate:
        s[component][name] = new_value

def generate_tap_secrets(s):
    input_field(s, "tap", "slack_webhook_url", "slack webhook url for querymonkey")
    input_file(s, "tap", "google_creds.json", "file containing google service account credentials")

def generate_log_secrets(s):
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
    set_generated_secret(s, "log", "username", "admin")
    set_generated_secret(s, "log", "password", admin[0])
    set_generated_secret(s, "log", "cookie", secrets.token_urlsafe(32))
    set_generated_secret(s, "log", "internal_users.yml", yaml.dump(internal_users))
    set_generated_secret(s, "log", "logstash-password", logstash[0])
    set_generated_secret(s, "log", "kibana-password", kibana[0])


def generate_postgres_secrets(s):
    set_generated_secret(s, "postgres", "exposurelog_password", secrets.token_hex(32))
    set_generated_secret(s, "postgres", "jupyterhub_password", secrets.token_hex(32))
    set_generated_secret(s, "postgres", "root_password", secrets.token_hex(64))


def generate_nublado2_secrets(s):
    crypto_key = ";".join([secrets.token_hex(32), secrets.token_hex(32)])
    set_generated_secret(s, "nublado2", "crypto_key", crypto_key)
    set_generated_secret(s, "nublado2", "proxy_token", secrets.token_hex(32))


def generate_nublado_secrets(s):
    crypto_key = ";".join([secrets.token_hex(32), secrets.token_hex(32)])
    set_generated_secret(s, "nublado", "jupyterhub_crypto_key", crypto_key)
    set_generated_secret(s, "nublado", "configproxy_auth_token", secrets.token_hex(32))

    # Pluck the password out of the postgres portion to generate our connect string.
    db_pass = s["postgres"]["jupyterhub_password"]
    session_db_url = f"postgres://jovyan:{db_pass}@postgres.postgres/jupyterhub"
    s["nublado"]["session_db_url"] = session_db_url


def generate_mobu_secrets(s):
    input_field(s, "mobu", "ALERT_HOOK", "Slack webhook for reporting mobu alerts.  Or use None for no alerting.")


def generate_cert_manager_secrets(s):
    input_field(s, "cert-manager", "aws-secret-access-key", "AWS secret access key for zone for DNS cert solver.")


def generate_gafaelfawr_secrets(s):
    key = rsa.generate_private_key(
        backend=default_backend(), public_exponent=65537, key_size=2048
    )

    key_bytes = key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    )

    set_generated_secret(s, "gafaelfawr", "redis-password", os.urandom(32).hex())
    set_generated_secret(s, "gafaelfawr", "session-secret", Fernet.generate_key().decode())
    set_generated_secret(s, "gafaelfawr", "signing-key", key_bytes.decode())

    auth_provider = input("Use cilogon or github? ")
    if auth_provider == "cilogon":
        input_field(s, "gafaelfawr", "cilogon-client-secret", "CILogon client secret")
    elif auth_provider == "github":
        input_field(s, "gafaelfawr", "github-client-secret", "GitHub client secret")
    else:
        raise Exception("Invalid auth provider")


def generate_pull_secret(s):
    input_file(s, "pull-secret", ".dockerconfigjson", ".docker/config.json to pull images")


def generate_ingress_nginx_secrets(s):
    input_file(s, "ingress-nginx", "tls.key", "Certificate private key")
    input_file(s, "ingress-nginx", "tls.crt", "Certificate chain")


def generate_argocd_secrets(s):
    pw = secrets.token_hex(16)
    h = bcrypt.hashpw(
        pw.encode("ascii"), bcrypt.gensalt(rounds=15)
    ).decode("ascii")
    now_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    set_generated_secret(s, "argocd", "admin.password", h)
    set_generated_secret(s, "argocd", "admin.passwordMtime", now_time)
    set_generated_secret(s, "argocd", "server.secretkey", secrets.token_hex(16))
    set_generated_secret(s, "enclave", "argocd.admin.plaintext_password", pw)


def load_current_secrets():
    s = defaultdict(dict)

    for f in Path('secrets').iterdir():
        print(f"Loading {f}")
        component = os.path.basename(f)
        s[component] = json.loads(f.read_text())

    return s

def generate_secrets():
    s = load_current_secrets()
    generate_pull_secret(s)
    generate_postgres_secrets(s)
    generate_log_secrets(s)
    generate_tap_secrets(s)
    generate_nublado_secrets(s)
    generate_nublado2_secrets(s)
    generate_mobu_secrets(s)
    generate_gafaelfawr_secrets(s)
    generate_argocd_secrets(s)

    use_cert_file = input("Use certificate file? (y/n): ")
    if use_cert_file == "y":
        generate_ingress_nginx_secrets(s)
    else:
        generate_cert_manager_secrets(s)

    return s


def generate_files(s):
    print("Generating secrets files in secrets/")
    os.makedirs("secrets", exist_ok=True)

    for k, v in s.items():
        with open(f"secrets/{k}", "w") as f:
            f.write(json.dumps(v))


if __name__ == "__main__":
    generate_files(generate_secrets())
