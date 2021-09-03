##########################################
Troubleshooting the Rubin Science Platform
##########################################

Intended audience: Anyone who is administering an installation of the Rubin Science Platform.

Sometimes things break, and we are assembling the most common failure scenarios, and their fixes, in this document.

PostgreSQL cannot mount its persistent volume
=============================================

**Symptoms:** When restarted, the ``postgres`` application pod fails to start because it cannot mount its persistent volume.
If the pod is already running, it gets I/O errors from its database, hangs, or otherwise shows signs of storage problems.

**Cause:** The ``postgres`` application requests a ``PersistentVolume`` via a ``PersistentVolumeClaim``.
If the backing store is corrupt or has been deleted or otherwise is disrupted, sometimes the ``PersistentVolume`` will become unavailable, but the ``PersistentVolumeClaim`` will hang on to it and keep trying to futilely mount it.
When this happens, you may need to recreate the persistent volume.

**Solution:** :doc:`../postgres/recreate-pvc`

Spawner menu missing images, cachemachine stuck pulling the same image
======================================================================

**Symptoms:** When a user goes to the spawner page for the Notebook Aspect, the expected menu of images is not available.
Instead, the menu is either empty or missing the right number of images of different classes.
The cachemachine service is continuously creating a ``DaemonSet`` for the same image without apparent forward progress.
Querying the cachemachine ``/available`` API shows either nothing in ``images`` or not everything that was expected.

**Cause:** Cachemachine is responsible for generating the menu used for spawning new JupyterLab instances.
The list of available images is pulled from the list of images that are already cached on every non-cordoned node to ensure that spawning will be quick.
If the desired types of images are not present on each node, cachemachine will create a ``DaemonSet`` for that image to attempt to start a pod using that image on every node, which will cache it.
If this fails to change the reported images available on each node, it will keep retrying.

The most common cause of this problem is a Kubernetes limitation.
By default, the Kubernetes list node API only returns the "first" (which usually means oldest) 50 cached images.
If more than 50 images are cached, images may go missing from that list even though they are cached, leading cachemachine to think they aren't cached and omitting them from the spawner menu.

**Solution:** :doc:`../cachemachine/pruning`

If this doesn't work, another possibility is that there is a node that cachemachine thinks is available for JupyterLab images but which is not eligible for its ``DaemonSet``.
This would be a bug in cachemachine, which should ignore cordoned nodes, but it's possible there is a new iteration of node state or a new rule for where ``DaemonSets`` are allowed to run that it does not know about.

Spawning a notebook fails with a pending error
==============================================

**Symptoms:** When a user tries to spawn a new notebook, the spawn fails with an error saying that the user's lab is already pending spawn or is pending deletion.

**Cause:** If the spawning of the lab fails or if the deletion of a lab fails, sometimes JupyterHub can give up on making further progress but still remember that the lab is supposedly still running.
In this case, JupyterHub may not recover without assistance.
You may need to delete the record for the affected user, and also make sure the user's lab namespace (visible in Argo CD under the ``nublado-users`` application) has been deleted.

**Solution:** :doc:`../nublado2/database`

User gets permission denied from services
=========================================

**Symptoms:** A user is able to authenticate to the Rubin Science Platform (prompted by going to the first authenticated URL, such as the Notebook Aspect spawner page), but then gets permission denied from other services.

**Causes:** Authentication and authorization to the Rubin Science Platform is done via a service called Gafaelfawr (see :doc:`../gafaelfawr`).
After the user authenticates, Gafaelfawr asks their authentication provider for the user's group memberships and then translates that to a list of scopes.
The mapping of group memberships to scopes is defined in the ``values.yaml`` file for Gafaelfawr for the relevant environment, in the ``gafaelfawr.config.groupMapping`` configuration option.

The most likely cause of this problem is that the user is not a member of a group that grants them access to that service.
Gafaelfawr will prevent the user from logging in at all if they are not a member of any group that grants access to a service.
If they are a member of at least one group, they'll be able to log in but may get permission denied errors from other services.

**Solution:** :doc:`../gafaelfawr/debugging`
