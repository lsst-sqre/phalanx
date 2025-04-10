# 1Password secrets bootstrap for the Phalanx CLI

The `.env` files in this directory provide a convenient and secure mechanism for accessing the `$OP_CONNECT_TOKEN` and `$VAULT_TOKEN` environment variables from 1Password for Phalanx environments managed by SQuaRE.
These secrets are required to use the `phalanx secrets` CLI.

To use these `.env` files, you need to have the [1Password CLI](https://developer.1password.com/docs/cli/) installed and signed into the correct 1Password Vault (LSST IT) with `op signin`.

Example usage:

```bash
op run --env-file="op/idfprod.env" -- phalanx secrets audit idfprod
```

Match the environment name in the `.env` file with the environment you are working with.
The `--` separates the command to be run from the options for `op run`.

See also: https://phalanx.lsst.io/admin/op-run-phalanx-cli.html
