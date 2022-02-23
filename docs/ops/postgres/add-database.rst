#####################
Adding a new database
#####################

From time to time you might need to add a new database to the internal
Postgres instance.

Before you do, please ask yourself how valuable the data is: the
internal Postgres is not intended to be either highly available or
extremely reliable.  It's designed for persistent storage for low-value
data, such as the JupyterHub session database, or Gafaelfawr's
authentication tokens, where the worst thing that happens, if it is
wiped out, is that a bunch of users lose their running sessions and have
to reauthenticate.

Assuming that the internal Postgres is indeed the right choice for your
needs, there are several steps.

=========================
Decide on a database name
=========================

In general the database will require three things: a database name, a
username, and a password.  Usually the database name and user should be
identical and should reflect the service that will consume the database,
e.g. ``gafaelfawr`` or ``exposurelog``.  We will use ``exposurelog`` as
the model for the remainder of this document.

==========================
Add the database to charts
==========================

First, create the entries in ``charts``.  Go to the
``charts/postgres/templates`` directory, and edit ``deployment.yaml`` to
add the new database/password entry.  You should copy an existing
entry, and it should look like this:

   .. code-block:: yaml

      {{- with .Values.exposurelog_db }}
      - name: VRO_DB_EXPOSURELOG_USER
        value: {{ .user }}
      - name: VRO_DB_EXPOSURELOG_DB
        value: {{ .db }}
      - name: VRO_DB_EXPOSURELOG_PASSWORD
        valueFrom:
          secretKeyRef:
            name: postgres
            key: exposurelog_password
      {{- end }}

Once you've done that, make sure you increment the chart version number in
``charts/postgres/Chart.yaml``.

===========================
Add the database to phalanx
===========================

Next, tackle ``phalanx``.  First, add the password entry to Phalanx's
installer, so the next time a new cluster is deployed or an extant
cluster is redeployed, the password will be created.  This belongs in
``installer/generate_secrets.py`` in the ``_postgres()`` method.

Typically we use passwords that are ASCII representations of random
32-byte hexadecimal sequences.  The passwords for all the non-root
Postgres users already look like that, so copying an existing line
and changing the name to reflect your service is usually correct:

   .. code-block:: python
    
      self._set_generated("postgres", "exposurelog_password", secrets.token_hex(32))

Make the Phalanx ``services/postgres/Chart.yaml`` entry depend on the
new chart version you earlier created.

Finally, go edit the postgres ``values-<env>.yaml`` files and add
a section for your new database with appropriate ``user`` and ``db``
entries:

   .. code-block:: yaml

      exposurelog_db:
        user: 'exposurelog'
        db: 'exposurelog'

Now start the PR and review process.  However, there is a step you still
must do before you can synchronize the updated services: put the
password into Vault so it appears in the postgres secrets.

================================
Manually add the secret to Vault
================================

Since you have already added generation of the password to the
installer, you could just generate new secrets for each environment and
push them into Vault.  That, however, would require that you restart
everything with randomly-generated passwords, and that's a fairly
disruptive operation, so you probably are better off manually injecting
just your new password.

* Consult ``1Password`` and retrieve the appropriate vault write token for
  the instance you're working with from ``vault_keys.json``.
* Set up your environment: ``export VAULT_ADDR=vault.lsst.codes ; export
  VAULT_FORMAT=json ; export VAULT_TOKEN=<retrieved-token>``
* Run ``vault kv patch secret/k8s_operator/<instance>/postgres
  <database-name>_password=$(openssl rand -hex 32)`` to generate and
  store a new random password.
* Delete the ``postgres`` secret from the ``postgres`` namespace to
  force Vault Secrets Operator to recreate it.
* Repeat for each environment where you need the new database.

=======================
Restart with new values
=======================

Now it's finally time to synchronize Postgres in each environment.

This will cause a brief service interruption in the cluster, so bear
that and your cluster's maintenance window policy in mind.

Much of the time, the restart of the ``postgres`` deployment gets stuck
and the old Pod will not terminate and allow the new one to run.  If
that happens, you need to identify the ReplicaSet responsible for the
stuck Pod, and delete that ReplicaSet.

Once Postgres restarts, the new database will be present, with the user
and password set.  At that point it is ready for use by your new service.
