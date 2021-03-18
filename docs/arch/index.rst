############
Architecture
############

Overview
========

Argo CD manages applications in the Rubin Science Platform through a set of Helm charts.
Which Helm charts to deploy in a given environment is controlled by the ``values-*.yaml`` files in `/science-platform <https://github.com/lsst-sqre/phalanx/tree/master/science-platform/>`__.

For nearly all charts, there are at least two layers of charts.
The upper layer of charts, the ones installed directly by Argo CD, are found in the `/services <https://github.com/lsst-sqre/phalanx/tree/master/services/>`__ directory.
These charts usually contain only dependencies and ``values-*.yaml`` files to customize the application for each environment.
Sometimes they may contain a small set of resources that are very specific to the Science Platform.

The real work of deploying an application is done by the next layer of charts, which are declared as dependencies (via the ``dependencies`` key in ``Chart.yaml``) of the top layer of charts.
By convention, the top-level chart has the same name as the underlying chart that it deploys.
This second layer of charts may be external third-party Helm charts provided by other projects, or may be Helm charts maintained by Rubin Observatory.
In the latter case, these charts are maintained in the `lsst-sqre/charts GitHub repository <https://github.com/lsst-sqre/charts/>`__.

Versioning
==========

The top level of charts defined in the ``/services`` directory are used only by Argo CD and are never published as Helm charts.
Their versions are therefore irrelevant.
The version of each chart is set to ``1.0.0`` because ``version`` is a required field in ``Chart.yaml`` and then never changed.
Reverting to a previous configuration in this layer of charts is done via a manual revert in Argo CD or by reverting a change in the GitHub repository, not by pointing Argo CD to an older chart.

The second layer of charts that are declared as dependencies are normal, published Helm charts that follow normal Helm semantic versioning conventions.
In the case of the lsst-sqre/charts repository, this is enforced by CI.
We can then constrain the version of the chart Argo CD will deploy by changing the ``dependencies`` configuration in the top-level chart.

Best practice is for a release of a chart to deploy the latest version of the corresponding application, so that upgrading the chart also implies upgrading the application.
This allows automatic creation of pull requests to upgrade any applications deployed by Argo CD (see `SQR-042 <https://sqr-042.lsst.io/>`__ for more details).
Charts maintained in lsst-sqre/charts follow this convention (for the most part).
Most upstream charts also follow this convention, but some require explicitly changing version numbers in ``values-*.yaml``.

In general, we pin the version of the chart to deploy in the ``dependencies`` metadata of the top-level chart.
This ensures deterministic cluster configuration and avoids inadvertently upgrading applications.
However, for services still under development, we sometimes use a floating dependency to reduce the number of pull requests required when iterating, and then switch to a pinned version once the service is stable.

There is currently no mechanism to deploy different versions of a chart in different environments.
We will probably need a mechanism to do this eventually, and have considered possible implementation strategies, but have not yet started on this work.
In the meantime, we disable automatic deployment in Argo CD so there is a human check on whether a given chart is safe to deploy in a given environment.

.. _hostnames:

Hostnames and TLS
=================

The Science Platform is designed to run under a single hostname.
All ingresses for all applications use different routes on the same external hostname.
That hostname, in turn, is served by an NGINX proxy web server, configured via the ``ingress-nginx`` Helm chart (normally installed with the Science Platform).
An NGINX ingress controller is required since its ``auth_request`` mechanism is used for authentication.

The external hostname must have a valid TLS certificate that is trusted by the stock configuration of standard CentOS, Debian, and Alpine containers.
There are supported two mechanisms to configure that TLS certificate:

#. Purchase a commercial certificate and configure it as the ingress-nginx default certificate.
   Do not add TLS configuration to any of the application ingresses.
   For more information, see :doc:`../ingress-nginx/certificates`.
   With this approach, the certificate will have to be manually renewed and replaced once per year.

#. Configure Let's Encrypt to obtain a certificate via the DNS solver.
   Once this is configured, TLS will be handled automatically without further human intervention.
   However, this approach is far more complex to set up and has some significant prerequisites.
   For more information, see :doc:`../cert-issuer/bootstrapping`.

To use the second approach, you must have the following:

* An :abbr:`AWS (Amazon Web Services)` account in which you can create two Route 53 hosted domains.
  You must use this domain for the hostname of the Science Platform installation.
* The ability to delegate to that Route 53 hosted domain from some public DNS domain.
  This means either registering a domain via Amazon, registering a domain elsewhere and pointing it to Amazon's Route 53 DNS servers, or creating a subdomain of an existing public domain by adding ``NS`` records to that domain for a subdomain hosted on Route 53.

If neither of those requirements sound familiar, you almost certainly want to use the first option and purchase a commercial certificate.

Ingress structure
-----------------

Because all application ingresses share the same external hostname, the way the ingress configuration is structured is somewhat unusual.

Nearly all of the services create an ingress without adding TLS configuration.
Instead, they all use the same hostname, without a TLS stanza.
The Nublado proxy ingress is the one designated ingress that has a TLS configuration and requests creation of certificates.
Because each ingress uses the same hostname, the NGINX ingress will merge all of those ingresses into one virtual host and will set up TLS if TLS is defined on any of them.

Were TLS defined on more than one ingress, only one of those TLS configurations would be used, but which one is chosen is somewhat random.
Therefore, we designate a single application to hold the configuration to avoid any confusion from unused configurations.

In the future, we are likely to move the TLS configuration to the landing page application instead of the Nublado proxy.
