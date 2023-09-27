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

Go to the `applications/postgres/templates <https://github.com/lsst-sqre/phalanx/tree/main/applications/postgres/templates>`__ directory and edit :file:`deployment.yaml` to add an entry for the new database.
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

Add the secret for the database
===============================

Both the ``postgres`` Phalanx application and any applications that talk to that database need to share a secret for the database password.

Pick one of the applications that uses the database as the primary owner for that password.
Add a new entry to :file:`secrets.yaml` for that password.
For example, the entry for the database password in the ``exposurelog`` application looks like this:

.. code-block:: yaml
   :caption: applications/exposurelog/secrets.yaml

   database-password:
     description: "Password for the exposurelog database."
     generate:
       type: password

Then, add an entry to `applications/postgres/secrets.yaml <https://github.com/lsst-sqre/phalanx/blob/main/applications/postgres/secrets.yaml>`__ that copies this secret into a ``postgres`` application secret.
For example:

.. code-block:: yaml
   :caption: applications/postgres/secrets.yaml

   exposurelog_password:
     description: "Password for the exposurelog database."
     if: exposurelog_db
     copy:
       application: exposurelog
       key: exposurelog_password

If any other applications also need to use the same database, add a similar entry to their :file:`secrets.yaml` files with a ``copy`` directive.

Generate the new secret and update the Vault secrets to include it by following the :doc:`standard secrets sync process </admin/sync-secrets>`.

Finally, edit the ``postgres`` :file:`values-{environment}.yaml` files for the environments that need this database and add a section for your new database with appropriate ``user`` and ``db`` entries:

.. code-block:: yaml
   :caption: applications/postgres/values-<environment>.yaml

   exposurelog_db:
     user: "exposurelog"
     db: "exposurelog"

Now start the PR and review process.

Restart with new values
=======================

Now it's finally time to synchronize PostgreSQL in each environment.
All you should need to do is sync the application in Argo CD.

This will cause a brief service interruption in the cluster while the deployment is recreated with additional environment variables and PostgreSQL restarts.
You may therefore want to wait for a maintenance window.

Once PostgreSQL restarts, the new database will be present, with the user and password set.
At that point it is ready for use by your new application.
