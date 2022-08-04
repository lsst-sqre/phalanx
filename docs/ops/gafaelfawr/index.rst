##########
Gafaelfawr
##########

.. list-table::
   :widths: 10,40

   * - Edit on GitHub
     - `/services/gafaelfawr <https://github.com/lsst-sqre/phalanx/tree/master/services/gafaelfawr>`__
   * - Type
     - Helm_
   * - Namespace
     - ``gafaelfawr``

.. rubric:: Overview

Gafaelfawr provides authentication and identity management services for the Rubin Science Platform.
It is primarily used as an NGINX ``auth_request`` handler configured via annotations on the ``Ingress`` resources of Science Platform services.
In that role, it requires a user have the required access scope to use that service, rejects users who do not have that scope, and redirects users who are not authenticated to the authentication process.

Gafaelfawr supports authentication via either OpenID Connect (often through `CILogon <https://cilogon.org/faq>`__) or GitHub.

Gafaelfawr also provides a token management API and (currently) UI for users of the Science Platform.

.. rubric:: Guides

.. toctree::

   debugging
   storage
   recreate-token
   github-organizations

.. seealso::

   * `DMTN-234: Identity management design <https://dmtn-234.lsst.io/>`__
   * `DMTN-224: Identity management implementation <https://dmtn-224.lsst.io/>`__
   * `SQR-069: Identity management history and decisions <https://sqr-069.lsst.io/>`__
   * `Gafaelfawr documentation <https://gafaelfawr.lsst.io/>`__
