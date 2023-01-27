#############################################################
Updating the Docker pull secret stored in 1Password and Vault
#############################################################

The pull secret, present in each RSP instance, and shared by many
applications there, is notoriously tricky to format correctly.

The recommended way to update it is to edit the pull secret in 1Password
and then deploy it with the ``installer/update-secrets.sh`` script;
however, this only works (at the time of writing, 20 May 2022) on Linux
systems with the 1Password 1.x CLI installed.

If you need to update the pull secret manually for an environment, here
are the important things to know:

You will first set the necessary environment variables:

* ``VAULT_ADDR`` must be set to ``https://vault.lsst.codes``
* ``VAULT_TOKEN`` must be set to the appropriate write token for the RSP
  instance.

Then you will construct the updated secret.  Just create a legal JSON
object.  The trick is, this value must be represented to Vault as a
*string*.  The easiest way to do this is:

#. Ensure the secret doesn't, itself, have any single quotes in it.  If
   it does, replace each single quote with ``'\''``
#. Copy the secret you've created into your paste buffer
#. Type ``vault kv patch secret/k8s_operator/<environment>/pull-secret
   .dockerconfigjson='``  (*nota bene*: that ends with a single quote)
#. Paste the secret into the command line
#. Type ``'`` and press Enter.

That will avoid the pain and hassle of multiple layers of quoting in
JSON objects, by handing the secret value as a (possibly multi-line)
string literal to Vault.

Then restart the ``vault-secrets-operator`` deployment and watch the pod
logs to make sure that pull-secret was correctly updated.

If you mess up, remember that our vault secrets are versioned, and you
can pull earlier versions of the secret with ``vault kv get secret
<path> -version <version>``; this (and the above technique) should let
you get back to a less-broken state.
