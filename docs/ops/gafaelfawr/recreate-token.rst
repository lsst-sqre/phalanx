####################################
Recreating Gafaelfawr service tokens
####################################

Where possible, we use persistent storage for Gafaelfawr's Redis database so that its tokens survive restarts and upgrades.
However, persistent storage isn't enabled for some clusters, such as (at the time of this writing) the yagan cluster at the summit.
On those clusters, if the ``gafaelfawr-redis`` service is restarted, its storage is cleared, and therefore all tokens will be invalidated.

When this happens, depending on the order of restart, the ``gafaelfawr-tokens`` pod that is responsible for maintaining service tokens in the cluster may not realize those tokens are no longer valid.
This will primarily affect the Notebook Aspect, which will be unable to authenticate to ``moneypenny`` and thus will not be able to spawn pods.
The result will be a "permission denied" error from moneypenny.

The easiest way to fix this problem is to force revalidation of all of the Gafaelfawr service tokens.
To do that:

#. Force a restart of the ``gafaelfawr-tokens`` deployment in the ``gafaelfawr`` namespace.
   This will recreate the secret in ``nublado2``.

#. Force a restart of the ``hub`` deployment in ``nublado2``.
   This will restart the hub with the new, correct token.

Be aware that when the Redis storage is wipoed, all user tokens will also be invalidated.
Users will be prompted to log in again the next time they go to the Science Platform.
