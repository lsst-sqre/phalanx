.. px-app-bootstrap:: cert-manager

##########################
Bootstrapping cert-manager
##########################

The issuer defined in the :px-app:`cert-manager` application uses the DNS solver.
The advantage of the DNS solver is that it works behind firewalls and can provision certificates for environments not exposed to the Internet, such as the Tucson teststand.
The DNS solver uses an AWS IAM user or role with write access to Route 53 to answer Let's Encrypt challenges.

In order to use ``cert-manager``, you must be hosting the DNS for the external hostname of the Science Platform installation in AWS Route 53.
See :doc:`/admin/hostnames` for more information.

Route 53 configuration
======================

First, ensure that ``cert-manager`` is set up for the domain in which the cluster will be hosted.
If this is a new domain, follow the instructions in :doc:`route53-setup`.

Then, in Route 53, create a CNAME from ``_acme-challenge.<cluster-name>`` to ``_acme-challenge.tls.<domain>`` where ``<domain>`` is the domain in which the cluster is located (such as ``lsst.codes`` or ``lsst.cloud``).
The new Route 53 dialog box makes this very confusing to do in the console.
Select **CNAME** from the lower drop-down menu and then **IP address or other value** from the top drop-down menu, and then you can enter ``_acme-challenge.tls.lsst.codes`` (for example) as the CNAME target.

For example, if the cluster name is ``data-dev.lsst.cloud``, create a CNAME record at ``_acme-challenge.data-dev.lsst.cloud`` whose value is ``_acme-challenge.tls.lsst.cloud``.
In the Route 53 console, the name of the record you create in the ``lsst.cloud`` hosted zone will be ``_acme-challenge.data-dev`` (yes, including the period).

.. warning::

   This approach is simple because the same CNAME and zone can be used for every hostname, but it means that simultaneous requests for TLS certificates for multiple hostnames will conflict and only one of the will succeed.
   cert-manager should make progress and eventually issue all of the certs, but if there are a large number of managed hostnames, consider using a more complicated structure with separate CNAME targets for each hostname in the ``tls`` zone.

This will need to be done for each hostname served by this instance of the RSP.
See :doc:`add-new-hostname` for a shorter version of these instructions to follow for each new hostname added.

Phalanx configuration
=====================

AWS federated auth
------------------

Add the following to the ``values-*.yaml`` file for an environment:

.. code-block:: yaml

   config:
     route53:
       roleArn: "<role-arn>"
       hostedZone: "<hosted-zone>"

``<hosted-zone>`` must correspond to the domain under which the cluster is hosted.
``<role-arn>`` is the ARN of an AWS IAM role that has permissions to modify records in the challenge zone.

Currently, only ``lsst.cloud`` is provisioned for AWS federated access:

.. code-block:: yaml

    roleArn: "arn:aws:iam::039289279626:role/phalanx-cert-manager-tls-lsst-codes"
    hostedZone: "Z0567328105IEHEMIXLCO"


AWS static auth
---------------

Add the following to the ``values-*.yaml`` file for an environment:

.. code-block:: yaml

   config:
     route53:
       awsAccessKeyId: "<access-key>"
       hostedZone: "<hosted-zone>"

``<hosted-zone>`` must correspond to the domain under which the cluster is hosted.
The values for the two most common Rubin Science Platform domains are:

.. code-block:: yaml

   lsst.codes:
     hostedZone: "Z06873202D7WVTZUFOQ42"
   lsst.cloud:
     hostedZone: "Z0567328105IEHEMIXLCO"

``<access-key>`` must correspond to the AWS IAM user that was created for this cluster to authenticate with AWS.

This key ID is for an AWS service user that has write access to the ``tls`` subdomain of the domain in which the cluster is hosted, and therefore can answer challenges.

Store the secret key for this AWS access key in Vault as the ``cert-manager`` secret for that cluster.
The Vault secret should look something like this:

.. code-block:: yaml

   data:
     aws-secret-access-key: "<secret>"

.. seealso::

   `cert-manager documentation for Route 53 <https://cert-manager.io/docs/configuration/acme/dns01/route53/>`__.
