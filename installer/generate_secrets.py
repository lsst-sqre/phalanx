#!/usr/bin/env python3
from base64 import b64encode
import bcrypt
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import json
import os
import secrets
import yaml


def input_field(component, name, description):
    prompt_string = f"[{component} {name}] ({description}): "
    return input(prompt_string)


def generate_tap_secrets():
    fname = input_field(
        "TAP",
        "google_creds.json",
        "file containing google service account credentials",
    )

    with open(fname, "r") as f:
        return {
            "slack_webhook_url": input_field(
                "TAP", "slack_webhook_url", "slack webhook url for querymonkey"
            ),
            "google_creds.json": b64encode(f.read().encode()).decode(),
        }


def generate_log_secrets():
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
    return {
        "username": "admin",
        "password": admin[0],
        "cookie": secrets.token_urlsafe(32),
        "internal_users.yml": yaml.dump(internal_users),
        "logstash-password": logstash[0],
        "kibana-password": kibana[0],
    }


def generate_postgres_secrets():
    return {
        "jupyterhub_password": secrets.token_hex(32),
        "root_password": secrets.token_hex(64),
    }


def generate_nublado2_secrets():
    return {
        "proxy_token": secrets.token_hex(32),
        "crypto_key": ";".join([secrets.token_hex(32), secrets.token_hex(32)]),
    }


def generate_nublado_secrets(db_pass):
    return {
        "configproxy_auth_token": secrets.token_hex(32),
        "jupyterhub_crypto_key": ";".join(
            [secrets.token_hex(32), secrets.token_hex(32)]
        ),
        "session_db_url": f"postgres://jovyan:{db_pass}@postgres.postgres/jupyterhub",
    }


def generate_mobu_secrets():
    return {
        "ALERT_HOOK": input_field(
            "mobu",
            "ALERT_HOOK",
            "Slack webhook for reporting mobu alerts.  Or use None for no alerting.",
        )
    }


def generate_cert_manager_secrets():
    return {
        "aws-secret-access-key": input_field(
            "cert-manager",
            "aws-secret-access-key",
            "AWS secret access key for zone for DNS cert solver.",
        )
    }


def generate_gafaelfawr_secrets():
    key = rsa.generate_private_key(
        backend=default_backend(), public_exponent=65537, key_size=2048
    )

    key_bytes = key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    )

    auth_provider = input_field(
        "gafaelfawr",
        "authentication provider",
        "Auth provider ('cilogon' or 'github')",
    ).lower()
    # maybe really validate this sometime
    if auth_provider != "github":
        auth_provider = "cilogon"

    ret_dict = {
        "redis-password": os.urandom(32).hex(),
        "session-secret": Fernet.generate_key().decode(),
        "signing-key": key_bytes.decode(),
    }

    if auth_provider == "cilogon":
        ret_dict["cilogon-client-secret"] = input_field(
            "gafaelfawr", "cilogon-client-secret", "CILogon client secret"
        )
    else:
        ret_dict["github-client-secret"] = input_field(
            "gafaelfawr", "github-client-secret", "GitHub client secret"
        )
    return ret_dict


def generate_pull_secret():
    fname = input_field(
        "[global]",
        ".docker/config.json",
        "file containing docker credentials to pull images",
    )

    with open(fname, "r") as f:
        return {".dockerconfigjson": f.read()}


def generate_secrets():
    secrets = {}
    secrets["pull-secret"] = generate_pull_secret()
    secrets["postgres"] = generate_postgres_secrets()
    secrets["log"] = generate_log_secrets()
    secrets["tap"] = generate_tap_secrets()
    secrets["nublado"] = generate_nublado_secrets(
        secrets["postgres"]["jupyterhub_password"]
    )
    secrets["nublado2"] = generate_nublado2_secrets()
    secrets["mobu"] = generate_mobu_secrets()
    secrets["gafaelfawr"] = generate_gafaelfawr_secrets()
    secrets["cert-manager"] = generate_cert_manager_secrets()

    return secrets


def generate_files(secrets):
    print("Generating secrets files in secrets/")
    os.makedirs("secrets", exist_ok=True)

    for k, v in secrets.items():
        with open(f"secrets/{k}", "w") as f:
            f.write(json.dumps(v))


if __name__ == "__main__":
    generate_files(generate_secrets())
