##########################################
Troubleshooting the Rubin Science Platform
##########################################

Intended audience: Anyone who is administering a Rubin Science Platform environment.

Sometimes things break, and we are assembling the most common failure scenarios, and their fixes, in this document.

PostgreSQL cannot mount its persistent volume
=============================================

**Symptoms:** When restarted, the ``postgres`` application pod fails to start because it cannot mount its persistent volume.
If the pod is already running, it gets I/O errors from its database, hangs, or otherwise shows signs of storage problems.

**Cause:** The ``postgres`` deployment requests a ``PersistentVolume`` via a ``PersistentVolumeClaim``.
If the backing store is corrupt or has been deleted or otherwise is disrupted, sometimes the ``PersistentVolume`` will become unavailable, but the ``PersistentVolumeClaim`` will hang on to it and keep trying to futilely mount it.
When this happens, you may need to recreate the persistent volume.

**Solution:** :ref:`recreate-postgres-pvc`

Spawner menu missing images, nublado stuck pulling the same image
=================================================================

**Symptoms:** When a user goes to the spawner page for the Notebook Aspect, the expected menu of images is not available.
Instead, the menu is missing one or more images.
The same image or set of images is pulled again each on each prepuller loop the nublado lab controller attempts.

**Solution:** :doc:`infrastructure/kubernetes-node-status-max-images`

Spawning a notebook fails with a pending error
==============================================

**Symptoms:** When a user tries to spawn a new notebook, the spawn fails with an error saying that the user's lab is already pending spawn or is pending deletion.

**Cause:** If the spawning of the lab fails or if the deletion of a lab fails, sometimes JupyterHub can give up on making further progress but still remember that the lab is supposedly still running.
In this case, JupyterHub may not recover without assistance.
You may need to delete the record for the affected user, and also make sure the user's lab namespace (visible in Argo CD under the ``nublado-users`` application) has been deleted.

**Solution:** :ref:`nublado2-clear-session-database`

User gets permission denied from applications
=============================================

**Symptoms:** A user is able to authenticate to the Rubin Science Platform (prompted by going to the first authenticated URL, such as the Notebook Aspect spawner page), but then gets permission denied from other application.

**Causes:** Authentication and authorization to the Rubin Science Platform is done via a application called :doc:`Gafaelfawr </applications/gafaelfawr/index>`.
After the user authenticates, Gafaelfawr asks their authentication provider for the user's group memberships and then translates that to a list of scopes.
The mapping of group memberships to scopes is defined in the ``values.yaml`` file for Gafaelfawr for the relevant environment, in the ``gafaelfawr.config.groupMapping`` configuration option.

The most likely cause of this problem is that the user is not a member of a group that grants them access to that application.
Gafaelfawr will prevent the user from logging in at all if they are not a member of any group that grants access to an application.
If they are a member of at least one group, they'll be able to log in but may get permission denied errors from other application.

**Solution:** :ref:`gafaelfawr-no-access`

You need privileged access to the filestore
===========================================

**Symptoms:** You need to do something like copy data from one instance to another, or to get a report of per-user usage on the filestore, or create a new non-world-writeable section under the filestore.

**Causes:** The RSP intentionally only lets you access a pod as an unprivileged user.
If you need to do something that spans users or should create root-owned files, you will need some way of accessing the filestore-presented filesystem with privilege.

**Solution:** :doc:`infrastructure/filestore/privileged-access`

User pods don't spawn, reporting "permission denied" from Moneypenny
====================================================================

**Symptoms:** A user pod fails to spawn, and the error message says that Moneypenny did not have permission to execute.

**Cause:** The ``gafaelfawr-token`` VaultSecret in the ``nublado2`` namespace is out of date.
This happened because the ``gafaelfawr-redis`` pod restarted and either it lacked persistent storage (at the T&S sites, as of July 2022), or because that storage had been lost.

**Solution:** :doc:`/applications/gafaelfawr/recreate-token`

Login fails with "bad verification code" error
==============================================

**Symptoms:** When attempting to authenticate to a Science Platform deployment using GitHub, the user gets the error message ``Authentication provider failed: bad_verification_code: The code passed is incorrect or expired.``

**Cause:** GitHub login failed after the OAuth 2.0 interaction with GitHub was successfully completed, and then the user reloaded the failed login page (or reloaded the page while Gafaelfawr was attempting to complete the authentication).
Usually this happens because Gafaelfawr was unable to write to its storage, either Redis or PostgreSQL.
If the storage underlying the deployment is broken, this can happen without producing obvious error messages, since the applications can go into disk wait and just time out.
Restarting the in-cluster ``postgresql`` pod, if PostgreSQL is running inside the Kubernetes deployment, will generally make this problem obvious because PostgreSQL will be unable to start.

**Solution:** Check the underlying storage for Redis and Gafaelfawr.
For in-cluster PostgreSQL, if this is happening for all users, try restarting the ``postgresql`` pod, which will not fix the problem but will make it obvious if it is indeed storage.
If the problem is storage, this will need to be escalated to whoever runs the storage for that Gafaelfawr deployment.

Note that reloading a failed login page from Gafaelfawr will never work and will always produce this error, so it can also be caused by user impatience.
In that case, the solution is to just wait or to return to the front page and try logging in again, rather than reloading the page.

User keeps logging in through the wrong identity provider
=========================================================

**Symptoms**: When attempting to use a different identity provider for authentication, such as when linking a different identity to the same account, the CILogon screen to select an identity provider doesn't appear.
Instead, the user is automatically sent to the last identity provider they used.

**Cause:** The CILogon identity provider selection screen supports remembering your selection, in which case it's stored in a browser cookie or local storage and you are not prompted again.
Even when you want to be prompted.

**Solution:** Have the user go to `https://cilogin.org/me <https://cilogon.org/me>`__ and choose "Delete ALL".
This will clear their remembered selection.
They can they retry whatever operation they were attempting.
