######################################################
Updating the pull secret stored in 1Password and Vault
######################################################

The pull secret, present in each RSP instance, and shared by many
services there, is notoriously tricky to format correctly.

The recommended way to update it is to edit the pull secret in 1Password
and then deploy it with the `installer/update-secrets.sh` script;
however, this only works (at the time of writing, 20 May 2022) on Linux
systems with the 1Password 1.x CLI installed.

If you need to update the pull secret manually for an environment, here
are the important things to know:

You will first set the necessary environment variables:

* ``VAULT_ADDR`` must be set to ``https://vault.lsst.codes``
* ``VAULT_TOKEN`` must be set to the appropriate write token for the RSP
  instance.

Then you will construct the updated secret in a file; for purposes of
this example, let's call it ``pull-secret.json``.  It should look like
this::

  { ".dockerconfigjson": "{\"auths\": {\"ghcr.io\": {\"auth\": \"base64string\", \"password\": \"cleartexttoken\",\"username\": \"token\"},\"index.docker.io\": {\"auth\":\"base64string\",\"password\":\"cleartextpassword\",\"username\":\"sqrereadonly\"}}}}

In short: the value is a *string* (not a JSON object) with all keys and
values quoted with backslash-escaped double quotes.

Once you have this file created, run:

``vault kv put secret/k8s_operator/<environment>/pull-secret @pull-secret.json``

Then restart the ``vault-secrets-operator`` deployment and watch the pod
logs to make sure that pull-secret was correctly updated.

If you mess up, remember than you can pull earlier versions of the
secret with ``vault kv get secret <path> -version <version>``; if you
set ``VAULT_FORMAT`` to ``json`` then you can just delete two (why two?
No idea) layers of ``data`` keys when you do this to create a new JSON
file you can then ``vault kv put`` back to restore the secret to the
original value.
