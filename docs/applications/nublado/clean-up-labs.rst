####################
Clean up broken labs
####################

It's possible for Nublado to accumulate broken labs.
In some extreme situations, such as load testing, there may be more labs than JupyterHub and the Nublado controller can manage, which then interferes with normal operations.

The most common cause of broken labs is that one of the services that creates labs for its own work has lost track of those labs or otherwise not shut them down properly.
Both :px-app:`mobu` and :px-app:`noteburst` are prone to this problem.

Deleting the lab
================

The first step to try is deleting the lab directly via :command:`kubectl`.
You can find the namespaces for all running labs with:

.. prompt:: bash

   kubectl get ns | grep ^nublado-

Be sure that you have configured :command:`kubectl` to look at the correct Phalanx environment.

The fastest way to delete an individual lab is to delete its namespace, which will clean up all of its resources:

.. prompt:: bash

   kubectl delete ns nublado-<username>

Replace ``<username>`` with the user whose lab you are deleting, which in the case of labs created by mobu or noteburst will generally start with ``bot-mobu`` or ``bot-noteburst``.

JupyterHub and the Nublado controller may not notice that the lab is no longer running immediately, since the Nublado controller does not query Kubernetes for the state of each lab constantly due to the load impact on the Kubernetes control plane.
The Nublado controller should recognize that the lab has been deleted the next time it reconciles its internal state with Kubernetes.
This is currently done every five minutes.

Purging lab records
===================

In more extreme situations, the number of labs could have overwhelmed JupyterHub, the Nublado controller, or both.
In this case, after deleting the labs, you will want to restart those services so that they rebuild their internal state.

Use the following procedure:

#. Delete the namespaces for all of the labs that are still running and need to be cleaned up.
   Wait for the namespace deletion to complete.
   This can take some time if there are a lot of labs and the Kubernetes control plane is busy.

#. Restart the Nublado controller (the ``nublado-controller`` deployment).
   This will force a reconciliation of its internal state against Kubernetes.
   It will now have an accurate list of which labs are currently running.

#. Restart JupyterHub (the ``hub`` deployment).
   On startup, it will query the Nublado controller for the status of every lab that it thinks is running and clean up its internal state when the Nublado controller tells it that lab does not exist.
