####################################
Recreating Gafaelfawr service tokens
####################################

Where possible, we use persistent storage for Gafaelfawr's Redis database so that its tokens survive restarts and upgrades.
However, if that persistent storage is deleted for some reason, or if Gafaelfawr is not configured to use persistent storage, all tokens will be invalidated.

When this happens, depending on the order of restart, the ``gafaelfawr-tokens`` pod that is responsible for maintaining service tokens in the cluster may take up to 30 minutes to realize those tokens are no longer valid.
This will primarily affect the Notebook Aspect, which will be unable to authenticate to the Nublado controller and thus will not be able to spawn pods.

Gafaelfawr will automatically fix this problem after 30 minutes, but unfortunately the JupyterHub component of ``nublado`` currently loads its token on startup and doesn't pick up changes.

The easiest way to fix this problem is to force revalidation of all of the Gafaelfawr service tokens.
To do that:

#. Force a restart of the ``gafaelfawr-tokens`` deployment in the ``gafaelfawr`` namespace.
   This will recreate any token secrets that are not valid.

#. Force a restart of the ``hub`` deployment in ``nublado``.
   This will restart the hub with the new, correct token.

Be aware that when the Redis storage is wipoed, all user tokens will also be invalidated.
Users will be prompted to log in again the next time they go to the Science Platform.

Invalidating the Redis storage will also result in inconsistencies between Redis and SQL that will produce nightly alerts if Gafaelfawr is configured to send Slack alerts.
To fix the inconsistencies, run ``gafaelfawr audit --fix`` inside the Gafaelfawr pod using ``kubectl exec``.
This will locate all the tokens that are no longer valid and mark them as expired in the database as well.
