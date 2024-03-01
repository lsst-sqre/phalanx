###############
Upgrading Vault
###############

Changing Vault configuration
============================

When making configuration changes, be aware that Argo CD will not detect a change to the configuration and automatically relaunch the ``vault-*`` pods.
You will need to delete the pods and let Kubernetes recreate them in order to pick up changes to the configuration.

If you change the number of HA replicas, Argo CD will fail to fully synchronize the configuration because the ``PodDisruptionBudget`` resource cannot be updated.
Argo CD will show an error saying that a resource failed to synchronize.
To fix this problem, delete the ``PodDisruptionBudget`` resource in Argo CD and then resynchronize the ``vault`` app, and then Argo CD will be happy.

Upgrade Process
===============

Unlike many applications managed by Argo CD, upgrading Vault requires manual intervention.

The Vault Helm chart is monitored by WhiteSource Renovate and can be upgraded via the normal pull requests that tool creates.
It will not change the version of the Vault software itself.
When merging an update, Argo CD will get confused about the upgrade status of Vault.
Fixing this will require the manual intervention explained below.
It's good practice to check if Vault itself has an update each time the Vault Helm chart is updated.

To upgrade Vault itself, first change the pinned version in the ``dependencies.version`` setting for Vault in `applications/vault/Chart.yaml <https://github.com/lsst-sqre/phalanx/blob/master/application/vault/Chart.yaml>`__.
Then, after that change is merged and you have synced Argo CD to apply the changes in Kubernetes, follow the `Vault upgrade instructions <https://developer.hashicorp.com/vault/docs/platform/k8s/helm/run#upgrading-vault-servers>`__.
You can skip the ``helm upgrade`` step, since Argo CD has already made the equivalent change.
Where those instructions say to delete a pod, deleting it through Argo CD works correctly.
You don't need to resort to ``kubectl``.
Kubernetes will not automatically upgrade the servers because the Vault ``StatefulSet`` uses ``OnDelete`` as the update mechanism.

After the upgrade is complete, you will notice that Argo CD thinks a deployment is in progress and will show the application as **Progressing** rather than **Healthy**.
This is due to an `Argo CD bug <https://github.com/argoproj/argo-cd/issues/1881>`__.
To work around that bug:

#. Open the Argo CD dashboard and locate the ``StatefulSet``.
   You will see two or more ``ControllerRevision`` resources with increasing versions, and three ``Pod`` resources.
   Check all the ``Pod`` resources and confirm they're running the latest revision.
   (This should be the end result of following the above-linked upgrade instructions.)
#. Delete the unused ``ControllerRevision`` objects using Argo CD, leaving only the latest that matches the revision the pods are running.
#. Delete one of the stand-by pods and let Kubernetes recreate it.
   See the Vault upgrade instructions above for how to identify which pods are stand-by.

This should clear the erroneous **Progressing** status in Argo CD.
