################
TLS certificates
################

The entire Science Platform uses the same external hostname and relies on NGINX merging all the ingresses into a single virtual host with a single TLS configuration.
As discussed in :ref:`hostnames`, TLS for the Science Platform can be configured with either a default certificate in ``ingress-nginx`` or through Let's Encrypt with the DNS solver.

If an installation is using Let's Encrypt with the DNS solver, no further configuration of the NGINX ingress is required.
See :px-app-bootstrap:`cert-manager` for setup information.

When using a commercial certificate, that certificate should be configured in the ``values-*.yaml`` for ``ingress-nginx`` for that environment.
Specifically, add the following under ``ingress-nginx.controller``:

.. code-block:: yaml

    extraArgs:
      default-ssl-certificate: "ingress-nginx/ingress-certificate"

And at the top level, add:

.. code-block:: yaml

   vaultCertificate:
     enabled: true

Then, in the Vault key named ``ingress-nginx`` in the Vault enclave for that environment, store the commercial certificate.
The Vault secret must have two keys: ``tls.crt`` and ``tls.key``.
The first must contain the full public certificate chain.
The second must contain the private key (without a passphrase).

For an example of an environment configured this way, see `/applications/ingress-nginx/values-minikube.yaml <https://github.com/lsst-sqre/phalanx/blob/master/applications/ingress-nginx/values-minikube.yaml>`__
