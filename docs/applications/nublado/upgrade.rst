.. px-app-upgrade:: nublado

#################
Upgrading Nublado
#################

Routine upgrades
================

There is currently a sequencing problem when syncing Nublado.
If it is synced in the obvious way, both JupyterHub and the Nublado controller restart at the same time.
If JupyterHub comes up first and the Nublado controller is unresponsive, it will decide that all running labs are invalid, making them inaccessible and forcing them to be shut down and respawned.

This is worth avoiding by syncing everything *except* the ``nublado-controller`` deployment first, and then syncing ``nublado-controller`` once JupyterHub is back up.
This ensures that the Nublado controller is running during the critical startup phase of JupyterHub.

Schema updates
==============

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
