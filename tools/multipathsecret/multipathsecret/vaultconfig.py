import hvac
import json
import os
from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class Keyset:
    '''Contains "accessor" and "id" tokens for a Vault path.
    '''
    accessor: str
    id: str


@dataclass
class Enclave:
    '''Maps a Vault path to 'read' and 'write' Keysets.  The 'Enclave' is
    simply a particular vault path with its own Keysets, e.g.
    'k8s_operator/nublado.lsst.codes'
    '''
    name: str
    read: Keyset
    write: Keyset


@dataclass
class VaultConfig:
    '''Contains the vault address (a URL represented as a string), the
    secret to be added, which is a dict mapping strings to strings
    (but can be None, if you're deleting a secret from a path), the
    rendered-to-memory JSON document representing all the vault paths
    and tokens, and the list of vault paths to not update.

    '''
    vault_address: str = os.getenv('VAULT_ADDR')
    secret: Optional[Dict[str, str]] = None
    enclaves: List[Enclave] = field(default_factory=list)
    skip_list: List[str] = field(default_factory=list)

    def __init__(self,
                 vault_address: Optional[str],
                 vault_file: str,
                 skip_list: Optional[List[str]],
                 secret_file: Optional[str] = None):
        if vault_address:
            self.vault_address = vault_address
        if secret_file:
            self.load_secret(secret_file)
        with open(vault_file, "r") as f:
            vault_dict = json.load(f)
        self.enclaves = []
        for item in vault_dict:
            name = list(item.keys())[0]
            if name in skip_list:
                continue
            read_k = Keyset(**item[name]["read"])
            write_k = Keyset(**item[name]["write"])
            enclave = Enclave(name=name, read=read_k, write=write_k)
            self.enclaves.append(enclave)

    def load_secret(self, secret_file: str) -> None:
        with open(secret_file, "r") as f:
            self.secret = json.load(f)

    def _get_write_key_for_enclave(self, enclave: Enclave) -> str:
        '''Given a Vault path, return its write key.
        '''
        return enclave.write.id

    def get_enclave_for_path(self, vault_path: str) -> Optional[Enclave]:
        '''Given a Vault path (e.g. 'k8s_operator/nublado.lsst.codes'),
        return the associated enlave.
        '''
        for enclave in self.enclaves:
            if enclave.name == vault_path:
                return enclave
            return None

    def add_secrets(self, secret_name: str, dry_run: bool = False) -> None:
        self._change_secrets(
            verb="add", secret_name=secret_name, dry_run=dry_run)

    def remove_secrets(self, secret_name: str, dry_run: bool = False) -> None:
        self._change_secrets(
            verb="remove", secret_name=secret_name, dry_run=dry_run)

    def _change_secrets(self, verb: str, secret_name: str,
                        dry_run: bool = False) -> None:
        for enclave in self.enclaves:
            self._change_secret(verb=verb, enclave=enclave,
                                secret_name=secret_name, dry_run=dry_run)

    def add_secret(self, enclave: Enclave, secret_name: str,
                   dry_run: bool = False) -> None:
        self._change_secret(verb="add", enclave=enclave,
                            secret_name=secret_name, dry_run=dry_run)

    def remove_secret(self, enclave: Enclave, secret_name: str,
                      dry_run: bool = False) -> None:
        self._change_secret(verb="remove", enclave=enclave,
                            secret_name=secret_name, dry_run=dry_run)

    def _change_secret(self, verb: str, enclave: Enclave, secret_name: str,
                       dry_run: bool = False) -> None:
        client = hvac.Client(url=self.vault_address)
        client.token = self._get_write_key_for_enclave(enclave)
        assert client.is_authenticated()
        secret_path = "{}/{}".format(enclave.name, secret_name)
        if verb not in ["add", "remove"]:
            raise RuntimeError("change_secret verb must be 'add' or 'remove'")
        if dry_run:
            print("Dry run: {} secret at ".format(verb) +
                  "{}/{}".format(self.vault_address,
                                 secret_path))
        else:
            if verb == "remove":
                client.secrets.kv.v2.delete_metadata_and_all_versions(
                    path=secret_path
                )
            else:
                client.secrets.kv.v2.create_or_update_secret(
                    path=secret_path,
                    secret=self.secret
                )
