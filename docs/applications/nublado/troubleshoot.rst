.. px-app-troubleshooting:: nublado

#######################
Troubleshooting Nublado
#######################

Check image prepulling status
=============================

Nublado will attempt to prepull all configured images to each node that it believes is allowed to run Nublado lab images.
To see the status of that prepulling, go to the ``/nublado/spawner/v1/prepulls`` route of the relevant environment.

In the resulting JSON document, ``config`` shows the current operative configuration, ``images`` shows the prepull status of the various images, and ``nodes`` shows the prepull status by node.

.. _nublado-clear-session-database:

Clear session database entry
============================

Historically, we sometimes saw JupyterHub get into an inconsistent state where it thought a pod was already running and couldn't be shut down.
We haven't seen this problem since switching to the Nublado controller, but it may still be possible for the JupyterHub session database to get out of sync.

If JupyterHub keeps telling a user that their lab is already spawning or shutting down, but doesn't allow them to connect to the lab or shut it down, following the instructions on `deleting a user session <https://nublado.lsst.io/admin/delete-user-session.html>`__ may fix the problem.

If it does, investigate how JupyterHub was able to get stuck.
This indicates some sort of bug in Nublado.

Prepuller is running continuously and/or expected menu items are missing
========================================================================

The Kubernetes control plane configuration variable ``nodeStatusMaxImages`` should be increased or disabled.
See :doc:`/admin/infrastructure/kubernetes-node-status-max-images`.
