.. px-app-upgrade:: nublado2

#################
Upgrading Nublado
#################

Most of the time, upgrading Nublado can be done simply by syncing the application in Argo CD.
There will be a brief outage for spawning new pods, but users with existing pods should be able to continue working.

Occasionally, new versions of JupyterHub will require a schema update.
We do not routinely enable automatic schema updates currently, so JupyterHub will refuse to start if a database schema update is required.
To enable schema updates, add:

.. code-block:: yaml

   jupyterhub:
     hub:
       db:
         upgrade: true

(The ``jupyterhub`` and ``hub`` keys probably already exist in the ``values-<environment>.yaml`` file, so just add the ``db.upgrade`` setting in the correct spot.)
Then, JupyterHub will automatically upgrade its database when the new version starts.
You can then remove this configuration again if you're worried about automatic updates misbehaving later.
