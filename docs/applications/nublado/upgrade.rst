.. px-app-upgrade:: nublado

#################
Upgrading Nublado
#################

Most of the time, upgrading Nublado can be done simply by syncing the application in Argo CD.
There will be a brief outage for spawning new pods, but users with existing pods should be able to continue working.

Occasionally, new versions of JupyterHub will require a schema update.
Automatic schema updates are off by default, so JupyterHub will refuse to start if a database schema update is required.

To enable schema updates, add the following to :file:`values-{environment}.yaml` for the ``nublado`` application:

.. code-block:: yaml

   jupyterhub:
     hub:
       db:
         upgrade: true

(The ``jupyterhub`` and ``hub`` keys probably already exist, so just add the ``db.upgrade`` setting in the correct spot.)
JupyterHub will then automatically upgrade its database when it is restarted running the new version.

You can then this configuration afterwards if you're worried about applying a schema update without being aware that you're doing so.

Alternately, for major upgrades to JupyterHub, you can choose to start from an empty database.
To do this, follow the instructions in the `Nublado documentation on wiping the database <https://nublado.lsst.io/admin/wipe-database.html>`__.
