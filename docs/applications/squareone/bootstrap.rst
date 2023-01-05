.. px-app-bootstrap:: squareone

#######################
Bootstrapping Squareone
#######################

By default, Squareone manages the TLS configuration for the entirety of the Science Platform.
This assumes the Let's Encrypt approach to obtaining TLS certificates, and the default TLS configuration requires the cert-manager cluster issuer be set up.
See :doc:`/applications/cert-manager/notes` for more information.

If you instead are using a commercial certificate and configuring ingress-nginx to use it, you need to disable the TLS configuration for Squareone.
Do that with the following in ``values-<environment>.yaml`` in `/applications/squareone <https://github.com/lsst-sqre/phalanx/tree/master/applications/squareone>`__:

.. code-block:: yaml

   ingress:
     tls: false
