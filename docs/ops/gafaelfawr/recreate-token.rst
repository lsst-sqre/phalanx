###############################
Recreating the gafaelfawr token
###############################

If Gafaelfawr has restarted and its ``redis`` service's storage has been
lost, services that rely on having a token from ``gafaelfawr`` to allow
them access to other services will no longer be able to authenticate.

This is seen in the ``nublado2`` namespace; when it happens the ``gafaelfawr-token`` no longer allows access to Moneypenny and user pod spawning fails.

To correct the issue:

#. Force a restart of the ``gafaelfawr-tokens`` deployment in the ``gafaelfawr`` namespace.  This will recreate the secret in ``nublado2``.

#. Force a restart of the ``hub`` deployment in ``nublado2``.  This will restart the hub with the new, correct token.
