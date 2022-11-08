.. px-app-upgrade:: cert-manager

######################
Upgrading cert-manager
######################

Upgrading :px-app:`cert-manager` is generally painless.
The only custom configuration that we use, beyond installing a cluster issuer, is to tell the Helm chart to install the Custom Resource Definitions.

Normally, it's not necessary to explicitly test :px-app:`cert-manager` after a routine upgrade.
We will notice if the certificates expire.
However, if you want to be sure that cert-manager is still working after an upgrade, delete the TLS secret and ``Certificate`` resource in the ``squareone`` namespace.
It should be recreated by cert-manager.

.. warning::

   This may cause an outage for the Science Platform since it is using this certificate, so you may want to be prepared to port-forward to get to the Argo CD UI in case something goes wrong.
