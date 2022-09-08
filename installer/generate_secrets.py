#!/usr/bin/env python3
import argparse
import base64
import json
import logging
import os
import secrets
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import bcrypt
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from onepassword import OnePassword


class SecretGenerator:
    """A basic secret generator that manages a secrets directory containing
    per-component secret export files from from Vault, as generated by
    read_secrets.sh.

    Parameters
    ----------
    environment : str
        The name of the environment (the environment's domain name).
    regenerate : bool
        If `True`, any secrets that can be generated by the SecretGenerator
        will be regenerated.
    """

    def __init__(self, environment, regenerate):
        self.secrets = defaultdict(dict)
        self.environment = environment
        self.regenerate = regenerate

    def generate(self):
        """Generate secrets for each component based on the `secrets`
        attribute, and regenerating secrets if applicable when the
        `regenerate` attribute is `True`.
        """
        self._pull_secret()
        self._rsp_alerts()
        self._butler_secret()
        self._postgres()
        self._tap()
        self._nublado2()
        self._mobu()
        self._gafaelfawr()
        self._argocd()
        self._portal()
        self._vo_cutouts()
        self._telegraf()
        self._sherlock()

        self.input_field("cert-manager", "enabled", "Use cert-manager? (y/n):")
        use_cert_manager = self.secrets["cert-manager"]["enabled"]
        if use_cert_manager == "y":
            self._cert_manager()
        elif use_cert_manager == "n":
            self._ingress_nginx()
        else:
            raise Exception(
                f"Invalid cert manager enabled value {use_cert_manager}"
            )

    def load(self):
        """Load the secrets files for each RSP component from the
        ``secrets`` directory.

        This method parses the JSON files and persists them in the ``secrets``
        attribute, keyed by the component name.
        """
        if Path("secrets").is_dir():
            for f in Path("secrets").iterdir():
                print(f"Loading {f}")
                component = os.path.basename(f)
                self.secrets[component] = json.loads(f.read_text())

    def save(self):
        """For each component, save a secret JSON file into the secrets
        directory.
        """
        os.makedirs("secrets", exist_ok=True)

        for k, v in self.secrets.items():
            with open(f"secrets/{k}", "w") as f:
                f.write(json.dumps(v))

    def input_field(self, component, name, description):
        default = self.secrets[component].get(name, "")
        prompt_string = (
            f"[{component} {name}] ({description}): [current: {default}] "
        )
        input_string = input(prompt_string)

        if input_string:
            self.secrets[component][name] = input_string

    def input_file(self, component, name, description):
        current = self.secrets.get(component, {}).get(name, "")
        print(f"[{component} {name}] ({description})")
        print(f"Current contents:\n{current}")
        prompt_string = "New filename with contents (empty to not change): "
        fname = input(prompt_string)

        if fname:
            with open(fname, "r") as f:
                self.secrets[component][name] = f.read()

    @staticmethod
    def _generate_gafaelfawr_token() -> str:
        key = base64.urlsafe_b64encode(os.urandom(16)).decode().rstrip("=")
        secret = base64.urlsafe_b64encode(os.urandom(16)).decode().rstrip("=")
        return f"gt-{key}.{secret}"

    def _get_current(self, component, name):
        if not self._exists(component, name):
            return None

        return self.secrets[component][name]

    def _set(self, component, name, new_value):
        self.secrets[component][name] = new_value

    def _exists(self, component, name):
        return component in self.secrets and name in self.secrets[component]

    def _set_generated(self, component, name, new_value):
        if not self._exists(component, name) or self.regenerate:
            self._set(component, name, new_value)

    def _tap(self):
        self.input_file(
            "tap",
            "google_creds.json",
            "file containing google service account credentials",
        )

    def _postgres(self):
        self._set_generated(
            "postgres", "exposurelog_password", secrets.token_hex(32)
        )
        self._set_generated(
            "postgres", "gafaelfawr_password", secrets.token_hex(32)
        )
        self._set_generated(
            "postgres", "jupyterhub_password", secrets.token_hex(32)
        )
        self._set_generated("postgres", "root_password", secrets.token_hex(64))
        self._set_generated(
            "postgres", "vo_cutouts_password", secrets.token_hex(32)
        )
        self._set_generated(
            "postgres", "narrativelog_password", secrets.token_hex(32)
        )

    def _nublado2(self):
        crypto_key = secrets.token_hex(32)
        self._set_generated("nublado2", "crypto_key", crypto_key)
        self._set_generated("nublado2", "proxy_token", secrets.token_hex(32))
        self._set_generated(
            "nublado2", "cryptkeeper_key", secrets.token_hex(32)
        )

        # Pluck the password out of the postgres portion.
        self.secrets["nublado2"]["hub_db_password"] = self.secrets["postgres"][
            "jupyterhub_password"
        ]

    def _mobu(self):
        self.input_field(
            "mobu",
            "ALERT_HOOK",
            "Slack webhook for reporting mobu alerts. "
            "Or use None for no alerting.",
        )

    def _cert_manager(self):
        self.input_field(
            "cert-manager",
            "aws-secret-access-key",
            "AWS secret access key for zone for DNS cert solver.",
        )

    def _gafaelfawr(self):
        key = rsa.generate_private_key(
            backend=default_backend(), public_exponent=65537, key_size=2048
        )

        key_bytes = key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        )

        self._set_generated(
            "gafaelfawr", "bootstrap-token", self._generate_gafaelfawr_token()
        )
        self._set_generated(
            "gafaelfawr", "redis-password", os.urandom(32).hex()
        )
        self._set_generated(
            "gafaelfawr", "session-secret", Fernet.generate_key().decode()
        )
        self._set_generated("gafaelfawr", "signing-key", key_bytes.decode())

        self.input_field("gafaelfawr", "cloudsql", "Use CloudSQL? (y/n):")
        use_cloudsql = self.secrets["gafaelfawr"]["cloudsql"]
        if use_cloudsql == "y":
            self.input_field(
                "gafaelfawr", "database-password", "Database password"
            )
        elif use_cloudsql == "n":
            # Pluck the password out of the postgres portion.
            db_pass = self.secrets["postgres"]["gafaelfawr_password"]
            self._set("gafaelfawr", "database-password", db_pass)
        else:
            raise Exception(
                f"Invalid gafaelfawr cloudsql value {use_cloudsql}"
            )

        self.input_field("gafaelfawr", "ldap", "Use LDAP? (y/n):")
        use_ldap = self.secrets["gaelfawr"]["ldap"]
        if use_ldap == "y":
            self.input_field("gafaelfawr", "ldap-password", "LDAP password")

        self.input_field("gafaelfawr", "auth_type", "Use cilogon or github?")
        auth_type = self.secrets["gafaelfawr"]["auth_type"]
        if auth_type == "cilogon":
            self.input_field(
                "gafaelfawr", "cilogon-client-secret", "CILogon client secret"
            )
            use_ldap = self.secrets["gafaelfawr"]["ldap"]
            if use_ldap == "y":
                self.input_field(
                    "gafaelfawr", "ldap-secret", "LDAP simple bind password"
                )
        elif auth_type == "github":
            self.input_field(
                "gafaelfawr", "github-client-secret", "GitHub client secret"
            )
        elif auth_type == "oidc":
            self.input_field(
                "gafaelfawr",
                "oidc-client-secret",
                "OpenID Connect client secret",
            )
            if use_ldap == "y":
                self.input_field(
                    "gafaelfawr", "ldap-secret", "LDAP simple bind password"
                )
        else:
            raise Exception(f"Invalid auth provider {auth_type}")

        if (
            self.secrets.get("rsp-alerts", {}).get("slack-webhook", None)
            is not None
        ):
            slack_webhook = self.secrets["rsp-alerts"]["slack-webhook"]
            if slack_webhook:
                self._set("gafaelfawr", "slack-webhook", slack_webhook)

    def _pull_secret(self):
        self.input_file(
            "pull-secret",
            ".dockerconfigjson",
            ".docker/config.json to pull images",
        )

    def _butler_secret(self):
        self.input_file(
            "butler-secret",
            "aws-credentials.ini",
            "AWS credentials for butler",
        )
        self.input_file(
            "butler-secret",
            "butler-gcs-idf-creds.json",
            "Google credentials for butler",
        )
        self.input_file(
            "butler-secret",
            "postgres-credentials.txt",
            "Postgres credentials for butler",
        )

    def _ingress_nginx(self):
        self.input_file("ingress-nginx", "tls.key", "Certificate private key")
        self.input_file("ingress-nginx", "tls.crt", "Certificate chain")

    def _argocd(self):
        current_pw = self._get_current(
            "installer", "argocd.admin.plaintext_password"
        )

        self.input_field(
            "installer",
            "argocd.admin.plaintext_password",
            "Admin password for ArgoCD?",
        )
        new_pw = self.secrets["installer"]["argocd.admin.plaintext_password"]

        if current_pw != new_pw or self.regenerate:
            h = bcrypt.hashpw(
                new_pw.encode("ascii"), bcrypt.gensalt(rounds=15)
            ).decode("ascii")
            now_time = datetime.now(timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            )

            self._set("argocd", "admin.password", h)
            self._set("argocd", "admin.passwordMtime", now_time)

        self.input_field(
            "argocd",
            "dex.clientSecret",
            "OAuth client secret for ArgoCD (either GitHub or Google)?",
        )

        self._set_generated(
            "argocd", "server.secretkey", secrets.token_hex(16)
        )

    def _telegraf(self):
        self.input_field(
            "telegraf",
            "influx-token",
            "Token for communicating with monitoring InfluxDB2 instance",
        )
        self._set("telegraf", "org-id", "square")

    def _portal(self):
        pw = secrets.token_hex(32)
        self._set_generated("portal", "ADMIN_PASSWORD", pw)

    def _vo_cutouts(self):
        self._set_generated(
            "vo-cutouts", "redis-password", os.urandom(32).hex()
        )

        self.input_field("vo-cutouts", "cloudsql", "Use CloudSQL? (y/n):")
        use_cloudsql = self.secrets["vo-cutouts"]["cloudsql"]
        if use_cloudsql == "y":
            self.input_field(
                "vo-cutouts", "database-password", "Database password"
            )
        elif use_cloudsql == "n":
            # Pluck the password out of the postgres portion.
            db_pass = self.secrets["postgres"]["vo_cutouts_password"]
            self._set("vo-cutouts", "database-password", db_pass)
        else:
            raise Exception(
                f"Invalid vo-cutouts cloudsql value {use_cloudsql}"
            )

        aws = self.secrets["butler-secret"]["aws-credentials.ini"]
        self._set("vo-cutouts", "aws-credentials", aws)
        google = self.secrets["butler-secret"]["butler-gcs-idf-creds.json"]
        self._set("vo-cutouts", "google-credentials", google)
        postgres = self.secrets["butler-secret"]["postgres-credentials.txt"]
        self._set("vo-cutouts", "postgres-credentials", postgres)

    def _sherlock(self):
        """This secret is for sherlock to push status to status.lsst.codes."""
        publish_key = secrets.token_hex(32)
        self._set_generated("sherlock", "publish_key", publish_key)

    def _rsp_alerts(self):
        """Shared secrets for alerting."""
        self.input_field(
            "rsp-alerts", "slack-webhook", "Slack webhook for alerts"
        )


class OnePasswordSecretGenerator(SecretGenerator):
    """A secret generator that syncs 1Password secrets into a secrets directory
    containing per-component secret export files from Vault (as generated
    by read_secrets.sh).

    Parameters
    ----------
    environment : str
        The name of the environment (the environment's domain name).
    regenerate : bool
        If `True`, any secrets that can be generated by the SecretGenerator
        will be regenerated.
    """

    def __init__(self, environment, regenerate):
        super().__init__(environment, regenerate)
        self.op_secrets = {}
        self.op = OnePassword()
        self.parse_vault()

    def parse_vault(self):
        """Parse the 1Password vault and store secrets applicable to this
        environment in the `op_secrets` attribute.

        This method is called automatically when initializing a
        `OnePasswordSecretGenerator`.
        """
        items = self.op.list_items("RSP-Vault")

        for i in items:
            key = None
            environments = []
            uuid = i["uuid"]
            doc = self.op.get_item(uuid=uuid)

            logging.debug(f"Looking at {uuid}")
            logging.debug(f"{doc}")

            for section in doc["details"]["sections"]:
                if "fields" not in section:
                    continue

                for field in section["fields"]:
                    if field["t"] == "generate_secrets_key":
                        if key is None:
                            key = field["v"]
                        else:
                            raise Exception(
                                "Found two generate_secrets_keys for {key}"
                            )
                    elif field["t"] == "environment":
                        environments.append(field["v"])

            # If we don't find a generate_secrets_key somewhere, then we
            # shouldn't bother with this document in the vault.
            if not key:
                logging.debug(
                    "Skipping because of no generate_secrets_key, %s", uuid
                )
                continue

            # The type of secret is either a note or a password login.
            # First, check the notes.
            secret_value = doc["details"]["notesPlain"]

            # If we don't find anything, pull the password from a login item.
            if not secret_value:
                for f in doc["details"]["fields"]:
                    if f["designation"] == "password":
                        secret_value = f["value"]

            logging.debug("Environments are %s for %s", environments, uuid)

            if self.environment in environments:
                self.op_secrets[key] = secret_value
                logging.debug("Storing %s (matching environment)", uuid)
            elif not environments and key not in self.op_secrets:
                self.op_secrets[key] = secret_value
                logging.debug("Storing %s (applicable to all envs)", uuid)
            else:
                logging.debug("Ignoring %s", uuid)

    def input_field(self, component, name, description):
        """Query for a secret's value from 1Password (`op_secrets` attribute).

        This method overrides `SecretGenerator.input_field`, which prompts
        a user interactively.
        """
        key = f"{component} {name}"
        if key not in self.op_secrets:
            raise Exception(f"Did not find entry in 1Password for {key}")

        self.secrets[component][name] = self.op_secrets[key]

    def input_file(self, component, name, description):
        """Query for a secret file from 1Password (`op_secrets` attribute).

        This method overrides `SecretGenerator.input_file`, which prompts
        a user interactively.
        """
        return self.input_field(component, name, description)

    def generate(self):
        """Generate secrets, updating the `secrets` attribute.

        This method first runs `SecretGenerator.generate`, and then
        automatically generates secrets for any additional components
        that were identified in 1Password.

        If a secret appears already, it is overridden with the value in
        1Password.
        """
        super().generate()

        for composite_key, secret_value in self.op_secrets.items():
            item_component, item_name = composite_key.split()
            # Special case for components that may not be present in every
            # environment, but nonetheless might be 1Password secrets (see
            # conditional in SecretGenerator.generate)
            if item_component in {"ingress-nginx", "cert-manager"}:
                continue

            logging.debug(
                "Updating component: %s/%s", item_component, item_name
            )
            self.input_field(item_component, item_name, "")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="generate_secrets")
    parser.add_argument(
        "--op",
        default=False,
        action="store_true",
        help="Load secrets from 1Password",
    )
    parser.add_argument(
        "--verbose", default=False, action="store_true", help="Verbose logging"
    )
    parser.add_argument(
        "--regenerate",
        default=False,
        action="store_true",
        help="Regenerate random secrets",
    )
    parser.add_argument("environment", help="Environment to generate")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig()

    if args.op:
        sg = OnePasswordSecretGenerator(args.environment, args.regenerate)
    else:
        sg = SecretGenerator(args.environment, args.regenerate)

    sg.load()
    sg.generate()
    sg.save()
