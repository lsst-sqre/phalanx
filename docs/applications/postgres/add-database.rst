#####################
Adding a new database
#####################

From time to time, you may need to add a new database to the internal PostgreSQL instance.

Before you do, ask yourself how valuable the data is.
The internal PostgreSQL service is not intended to be highly available or extremely reliable.
It's designed for persistent storage for low-value data such as the JupyterHub session database, where the worst thing that happens after data loss is that users lose running sessions and may have to reauthenticate.

Assuming that the internal PostgreSQL is indeed the right choice for your needs, there are several steps.

Decide on a database name
=========================

The service requires a database name, a username, and a password.
Usually the database name and user should be identical and should match the application that will consume the database (for example, ``gafaelfawr`` or ``exposurelog``).
We will use ``exposurelog`` as the model for the remainder of this document.

Add the database to the deployment
==================================

Go to the ``/services/postgres/templates`` directory and edit ``deployment.yaml`` to add an entry for the new database.
You should copy an existing entry to get the syntax correct, and then change the names.
The result should look like this:

.. code-block:: yaml

   {{- with .Values.exposurelog_db }}
   - name: VRO_DB_EXPOSURELOG_USER
     value: {{ .user }}
   - name: VRO_DB_EXPOSURELOG_DB
     value: {{ .db }}
   - name: VRO_DB_EXPOSURELOG_PASSWORD
     valueFrom:
       secretKeyRef:
         name: "postgres"
         key: "exposurelog_password"
   {{- end }}

Add the database to Phalanx installer
=====================================

Add a password entry to Phalanx's installer, so the next time a new cluster is deployed or an extant cluster is redeployed, the password will be created.
This belongs in ``installer/generate_secrets.py`` in the ``_postgres()`` method.

Typically, we use passwords that are ASCII representations of random 32-byte hexadecimal sequences.
The passwords for all the non-root PostgreSQL users already look like that, so copying an existing line and changing the name to reflect your application is usually correct:

.. code-block:: python
   :caption: /installer/generate_secrets.py

   self._set_generated("postgres", "exposurelog_password", secrets.token_hex(32))

Finally, edit the ``postgres`` ``values-<environment>.yaml`` files for the environments that need this database and add a section for your new database with appropriate ``user`` and ``db`` entries:

.. code-block:: yaml
   :caption: /services/postgres/values-<environment>.yaml

   exposurelog_db:
     user: "exposurelog"
     db: "exposurelog"

Now start the PR and review process.

Manually add the secret to Vault
================================

Since you have already added generation of the password to the installer, you could just generate new secrets for each environment and push them into Vault.
That, however, would require that you restart everything with randomly-generated passwords, and that's a fairly disruptive operation, so you probably are better off manually injecting just your new password.

.. rst-class:: open

#. Consult 1Password and retrieve the appropriate vault write token for the instance you're working with from ``vault_keys.json``.

#. Set up your environment:

   .. code-block:: bash

      export VAULT_ADDR=vault.lsst.codes
      export VAULT_TOKEN=<retrieved-token>

#. Generate and store a new random password:

   .. code-block:: bash

      vault kv patch secret/k8s_operator/<instance>/postgres \
          <database-name>_password=$(openssl rand -hex 32)

#. Delete the ``postgres`` ``Secret`` from the ``postgres`` namespace to force Vault Secrets Operator to recreate it.

#. Repeat for each environment where you need the new database.

Restart with new values
=======================

Now it's finally time to synchronize PostgreSQL in each environment.
All you should need to do is sync the application in Argo CD.

This will cause a brief service interruption in the cluster while the deployment is recreated with additional environment variables and PostgreSQL restarts.
You may therefore want to wait for a maintenance window.

Once PostgreSQL restarts, the new database will be present, with the user and password set.
At that point it is ready for use by your new application.
