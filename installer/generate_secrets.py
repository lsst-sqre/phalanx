#!/usr/bin/env python3
from base64 import b64encode
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import json
import os
import secrets


def input_field(component, name, description):
  prompt_string = f"[{component} {name}] ({description}): "
  return input(prompt_string)

def generate_tap_secrets():
  fname = input_field("TAP", "google_creds.json",
    "file containing google service account credentials")

  with open(fname, 'r') as f:
    return {
      "slack_webhook_url": input_field("TAP", "slack_webhook_url",
        "slack webhook url for querymonkey"),
      "google_creds.json": b64encode(f.read().encode()).decode()
    }

def generate_postgres_secrets():
  return {
    "jupyterhub_password": secrets.token_hex(32),
    "root_password": secrets.token_hex(64),
  }

def generate_nublado_secrets(db_pass):
  return {
    "configproxy_auth_token": secrets.token_hex(32),
    "jupyterhub_crypto_key": ";".join([secrets.token_hex(32), secrets.token_hex(32)]),
    "session_db_url": f"postgres://jovyan:{db_pass}@postgres.postgres/jupyterhub",
  }

def generate_mobu_secrets():
  return {
    "ALERT_HOOK": input_field("mobu", "ALERT_HOOK",
      "Slack webhook for reporting mobu alerts.  Or use None for no alerting.")
  }

def generate_cert_manager_secrets():
  return {
    "aws-secret-access-key": input_field("cert-manager",
      "aws-secret-access-key",
      "AWS secret access key for AKIAQSJOS2SFLUEVXZDB for DNS cert solver.")
  }

def generate_gafaelfawr_secrets():
  key = rsa.generate_private_key(
    backend=default_backend(),
    public_exponent=65537,
    key_size=2048
  )

  key_bytes = key.private_bytes(
    serialization.Encoding.PEM,
    serialization.PrivateFormat.PKCS8,
    serialization.NoEncryption()
  )

  return {
    "cilogon-client-secret": input_field("gafaelfawr", "cilogon-client-secret",
                                         "CILogon client secret"),
    "session-secret": Fernet.generate_key().decode(),
    "signing-key": key_bytes.decode(),
  }

def generate_secrets():
  secrets = {}
  secrets["postgres"] = generate_postgres_secrets()
  secrets["tap"] = generate_tap_secrets()
  secrets["nublado"] = generate_nublado_secrets(secrets["postgres"]["jupyterhub_password"])
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

if __name__ == '__main__':
  generate_files(generate_secrets())
