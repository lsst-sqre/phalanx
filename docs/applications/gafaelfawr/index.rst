.. px-app:: gafaelfawr

######################################
gafaelfawr — Authentication & identity
######################################

Gafaelfawr provides authentication and identity management services for the Rubin Science Platform.
It is primarily used as an NGINX ``auth_request`` handler configured via annotations on the ``Ingress`` resources of Science Platform services.
In that role, it requires a user have the required access scope to use that service, rejects users who do not have that scope, and redirects users who are not authenticated to the authentication process.

Gafaelfawr supports authentication via either OpenID Connect (often through CILogon_) or GitHub.

Gafaelfawr also provides a token management API and (currently) UI for users of the Science Platform.

.. jinja:: gafaelfawr
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 2

   bootstrap
   manage-schema
   quotas
   recreate-token
   add-oidc-client
   github-organizations
   troubleshoot
   values
