##########################
Bootstrapping cert-manager
##########################

The issuer defined in the ``cert-manager`` service uses the DNS solver.
The advantage of the DNS solver is that it works behind firewalls and can provision certificates for environments not exposed to the Internet, such as the Tucson teststand.
The DNS solver uses an AWS service user with write access to Route 53 to answer Let's Encrypt challenges.

In order to use ``cert-manager``, you must be hosting the DNS for the external hostname of the Science Platform installation in AWS Route 53.
See :ref:`hostnames` for more information.

First, ensure that ``cert-manager`` is set up for the domain in which the cluster will be hosted.
If this is a new domain, follow the instructions in :doc:`route53-setup`.

Then, in Route 53, create a CNAME from ``_acme-challenge.<cluster-name>`` to ``_acme-challenge.tls.<domain>`` where ``<domain>`` is the domain in which the cluster is located (such as ``lsst.codes`` or ``lsst.cloud``).
The new Route 53 dialog box makes this very confusing to do in the console.
Select **CNAME** from the lower drop-down menu and then **IP address or other value** from the top drop-down menu, and then you can enter ``_acme-challenge.tls.lsst.codes`` (for example) as the CNAME target.

For example, if the cluster name is ``data-dev.lsst.cloud``, create a CNAME record at ``_acme-challenge.data-dev.lsst.cloud`` whose value is ``_acme-challenge.tls.lsst.cloud``.
In the Route 53 console, the name of the record you create in the ``lsst.cloud`` hosted zone will be ``_acme-challenge.data-dev`` (yes, including the period).

Add the following to the ``values-*.yaml`` file for an environment:

.. code-block:: yaml

   config:
     route53:
       awsAccessKeyId: "<access-key>"
       hostedZone: "<hosted-zone>"

``<access-key>`` and ``<hosted-zone>`` must correspond to the domain under which the cluster is hosted.
The values for the two most common Rubin Science Platform domains are:

.. code-block:: yaml

   lsst.codes:
     awsAccessKeyId: "AKIAQSJOS2SFLUEVXZDB"
     hostedZone: "Z06873202D7WVTZUFOQ42"
   lsst.cloud:
     awsAccessKeyId: "AKIAQSJOS2SFKQBMDRGR"
     hostedZone: "Z0567328105IEHEMIXLCO"

This key ID is for an AWS service user that has write access to the ``tls`` subdomain of the domain in which the cluster is hosted, and therefore can answer challenges.

Finally, store the secret key for this AWS access key in Vault as the ``cert-manager`` secret for that cluster.
The Vault secret should look something like this:

.. code-block:: yaml

   data:
     aws-access-key-id: "<access-key>"
     aws-secret-access-key: "<secret>"

The secrets for the SQuaRE-maintained Rubin Science Platform domains are stored in 1Password (search for ``cert-manager-lsst-codes`` or ``cert-manager-lsst-cloud``).
If this cluster is in the same domain as another, working cluster, you can copy the secret from that cluster into the appropriate path for the new cluster.
