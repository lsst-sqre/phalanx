###########################################
Updating the pull secret for an environment
###########################################

.. warning::

   These instructions are only for updating the pull secret directly in Vault.
   For environments that use 1Password as a source for static secrets, see :ref:`admin-onepassword-pull-secret` for instructions on how to create or modify the 1Password item containing the pull secret.

The pull secret, present in each RSP instance, and shared by many applications there, is notoriously tricky to format correctly.
If you need to update the pull secret manually for an environment, here are the important things to know:

You will first set the necessary environment variables:

* ``VAULT_ADDR`` must be set to ``https://vault.lsst.codes``
* ``VAULT_TOKEN`` must be set to the appropriate write token for the RSP environment

Then, construct the updated secret as a JSON object.
This will normally involve adding a new hostname to the ``auths`` section containing ``username``, ``password``, and ``auth`` keys, where the value of the ``auth`` key is the base64-encoded version of the username and password separated by a colon.
See `Pull an image from a private registry <https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/>`__ in the Kubernetes documentation for more details about the correct format.

Once you have the new JSON object, store it in Vault.
This value must be represented to Vault as a *string*.
The easiest way to do this is:

#. Ensure the secret doesn't, itself, have any single quotes in it.
   If it does, replace each single quote with ``'\''``
#. Copy the secret you've created into your paste buffer.
#. Type ``vault kv patch secret/k8s_operator/<environment>/pull-secret .dockerconfigjson='`` (*nota bene*: that ends with a single quote).
#. Paste the secret into the command line.
#. Type ``'`` and press Enter.

That will avoid the pain and hassle of multiple layers of quoting in JSON objects by handing the secret value as a string literal to Vault.

Then restart the ``vault-secrets-operator`` deployment and watch the pod logs to make sure that the ``Secret`` named ``pull-secret`` was correctly updated.

If you mess up, remember that our vault secrets are versioned, and you can pull earlier versions of the secret with ``vault kv get secret <path> -version <version>``; this (and the above technique) should let you get back to a less-broken state.
