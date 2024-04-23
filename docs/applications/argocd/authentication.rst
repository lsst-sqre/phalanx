######################
Argo CD authentication
######################

Argo CD supports three main methods of authentication: the ``admin`` account, local accounts, or SSO (Single Sign-On).
We use the ``admin`` account plus SSO.

Argo CD documentation recommends disabling the ``admin`` account once user access via SSO is configured.
We've chosen to ignore that advice in favor of having an easy and reliable emergency access mechanism that doesn't rely on any other service, and have instead created strong, randomized ``admin`` passwords.
Still, normal Argo CD access should be done via SSO, both to minimize use of the ``admin`` password and for attribution of actions taken via the web UI.

In SQuaRE-run environments hosted on Google Kubernetes Engine, Argo CD is configured to use Google OAuth for SSO using the same Google Cloud Identity domain (``lsst.cloud``) as is used for other Google operations.
On some Telescope and Site environments (eventually, all of them), Argo CD is configured to use Keycloak for SSO.
On all other installations, Argo CD is configured to use GitHub.

.. note::

   We do not use :doc:`Gafaelfawr <../gafaelfawr/index>` to protect Argo CD even though it would be capable of doing so because we want access to the cluster management UI to be independent of anything else running in the cluster.
   Argo CD is how we prefer to fix Gafaelfawr if it is broken, so it is configured to authenticate users directly and independently.

Configuring Google SSO
======================

To set up Google SSO authentication to Argo CD in a new cluster, take the following steps as a user with the ``roles/oauthconfig.editor`` role:

#. On the GCP console, go to :guilabel:`OAuth consent screen` under :guilabel:`APIs & Services`.

#. Select :guilabel:`Internal` and click :guilabel:`Create`.

#. Enter the environment information.
   For example (adjust for the environment):
   - App name: Rubin Science Platform (int)
   - User support email: Choose the address of the person doing this
   - Application home page: https://data-int.lsst.cloud/
   - Authorized domains: lsst.cloud
   - Developer contact information email addresses: Work email address

#. Click :guilabel:`Save and Continue`.

#. Add the ``openid`` scope and click :guilabel:`Save and Continue`.

#. Click :guilabel:`Back to Dashboard`.

#. Go to :guilabel:`Credentials` still under :guilabel:`APIs & Services`.

#. Click :guilabel:`Create Credentials` and choose :guilabel:`OAuth client ID`.

#. Choose :guilabel:`Web application` as the application type.

#. Enter "Argo CD" as the name.

#. Add the ``/argo-cd/api/dex/callback`` route under "Authorized redirect URIs."
   For example: ``https://data-int.lsst.cloud/argo-cd/api/dex/callback``

#. Click on :guilabel:`Create`.
   This will pop up a dialog with the client ID and secret for the newly-created OAuth client.

#. Store this secret as the ``dex.clientSecret`` key in the secret for the ``argocd`` application in your :ref:`static secrets store <admin-static-secrets>`, however those secrets are stored for your environment.
   Then, sync secrets for your environment.

#. In the Phalanx repository, under :file:`applications/argocd`, edit the :file:`values-{environment}.yaml` file for the relevant environment.
   In ``argo-cd.configs.cm``, at the same level as ``url``, add the following, modifying the URLs and ``hostedDomains`` for the environment and changing the ``clientID`` to the value from the pop-up:

   .. code-block:: yaml

      dex.config: |
        connectors:
          # Auth using Google.
          # See https://dexidp.io/docs/connectors/google/
          - type: google
            id: google
            name: Google
            config:
              clientID: <client-id-from-dialog-box>
              clientSecret: $dex.clientSecret
              hostedDomains:
                - lsst.cloud
              redirectURI: https://data-int.lsst.cloud/argo-cd/api/dex/callback

   The value for ``clientSecret`` should literally be ``$dex.clientSecret``, which tells Argo CD to get it from the Argo CD configuration secret.

#. In the same file, add a new ``argo-cd.configs.rbac`` key as follows:

   .. code-block:: yaml

      rbac:
        policy.csv: |
          g, adam@lsst.cloud, role:admin
          g, afausti@lsst.cloud, role:admin
          g, frossie@lsst.cloud, role:admin
          g, jsick@lsst.cloud, role:admin
          g, rra@lsst.cloud, role:admin
        scopes: "[email]"

   Change the list of users to the email addresses of the users who should have admin access to this environment.

#. If the environment already exists, create a PR with the above changes, merge it, and then sync Argo CD.

#. Go to the ``/argo-cd`` route on the environment.
   Log out if you're logged in with the admin password.
   You should see a login in with Google option appear.
   Click on it and you should be able to authenticate with Google.
   Anyone in the same hosted domain can authenticate, but if you aren't one of the listed users, you should not see any applications.

Configuring Keycloak SSO
========================

To set up Keycloak SSO authentication to Argo CD in a new cluster, take the following steps:

#. Follow the `Argo CD documentation <https://argo-cd.readthedocs.io/en/stable/operator-manual/user-management/keycloak/>`__ to create a Keycloak client for Argo CD.
   Ensure group information is released by Keycloak, following the instructions in the above page.

   We found that the :guilabel:`Valid redirect URIs` setting has to use the wildcard pattern described as less secure or it wouldn't work correctly.

   Argo CD uses the expiration time of the access token as the length of the session, so ensure that its lifetime is reasonable (two hours, for example).

#. Store the secret for the Keycloak client as the ``dex.clientSecret`` key in the secret for the ``argocd`` application in your :ref:`static secrets store <admin-static-secrets>`, however those secrets are stored for your environment.
   Then, sync secrets for your environment.

#. In the Phalanx repository, under :file:`applications/argocd`, edit the :file:`values-{environment}.yaml` file for the relevant environment.
   In ``argo-cd.configs.cm``, at the same level as ``url``, add the following, modifying the URL to match the Keycloak server that should be used:

   .. code-block:: yaml

      oidc.config: |
        name: Keycloak
        issuer: https://keycloak.example.org/realms/master
        clientID: argocd
        clientSecret: $dex.clientSecret
        requestedScopes: ["openid", "profile", "email", "groups"]

   Adjust ``clientID`` if you chose a different name for the Keycloak client.
   The value for ``clientSecret`` should literally be ``$dex.clientSecret``, which tells Argo CD to get it from the Argo CD configuration secret.

#. Determine the group memberships that should control access to Argo CD.
   Then, in the same file, add a new ``argo-cd.configs.rbac`` key as follows:

   .. code-block:: yaml

      rbac:
        policy.csv: |
          g, admin-group, role:admin
          g, readonly-group, role:readonly

   Change the group names and roles according to the access policy that you want for this instance of Argo CD.
   See :ref:`argocd-access-control` for more details.

#. If the environment already exists, create a PR with the above changes, merge it, and then sync Argo CD.

#. Go to the ``/argo-cd`` route on the environment.
   Log out if you're logged in with the admin password.
   You should see a login in with Keycloak option appear.
   Click on it and you should be able to authenticate with Keycloak.
   Any valid Keycloak user should be able to authenticate, but your subsequent access should depend on your group membership and the access control rules configured above.

Configuring GitHub SSO
======================

To set up Google SSO authentication to Argo CD in a new cluster, take the following steps:

#. From the GitHub page of the organization in which you want to create the OAuth application (such as `lsst-sqre <https://github.com/lsst-sqre>`__), go to :menuselection:`Settings --> Developer Settings --> OAuth Apps`.

#. Click :guilabel:`New OAuth App`.

#. Enter the following information (adjust for the environment):
   - Application name: ``RSP Argo CD (IDF-int)``
   - Homepage URL: ``https://data-int.lsst.cloud/argo-cd``
   - Authorization callback URL: ``https://data-int.lsst.cloud/argo-cd/api/dex/callback``

#. Click :guilabel:`Register Application`.

#. Click :guilabel:`Generate a new client secret`.

#. Store this secret as the ``dex.clientSecret`` key in the secret for the ``argocd`` application in your :ref:`static secrets store <admin-static-secrets>`, however those secrets are stored for your environment.
   Then, sync secrets for your environment.

#. In the Phalanx repository, under :file:`applications/argocd`, edit the :file:`values-{environment}.yaml` file for the relevant environment.
   In ``argo-cd.configs.cm``, at the same level as ``url``, add the following, modifying the URL for the environment and changing the ``clientID`` to the value from GitHub:

   .. code-block:: yaml

      dex.config: |
        connectors:
          # Auth using GitHub.
          # See https://dexidp.io/docs/connectors/github/
          - type: github
            id: github
            name: GitHub
            config:
              clientID: <client-id>
              # Reference to key in argo-secret Kubernetes resource
              clientSecret: $dex.clientSecret
              orgs:
                - name: lsst-sqre

   The value for ``clientSecret`` should literally be ``$dex.clientSecret``, which tells Argo CD to get it from the Argo CD configuration secret.
   Adjust the ``orgs`` list if needed to allow access to different GitHub organizations.

#. In the same file, add a new ``argo-cd.configs.cm.rbac`` key as follows:

   .. code-block:: yaml

      rbacConfig:
        policy.csv: |
          g, lsst-sqre:square, role:admin

   Add lines for additional GitHub teams as needed for that environment.
   Be aware that this uses the human-readable name of the team (with capital letters and spaces if applicable), not the slug.

#. If the environment already exists, create a PR with the above changes, merge it, and then sync Argo CD.

#. Go to the ``/argo-cd`` route on the environment.
   Log out if you're logged in with the admin password.
   You should see a login in with GitHub option appear.
   Click on it and you should be able to authenticate with GitHub.
   Anyone in the same GitHub organization can authenticate, but if you aren't in one of the listed teams, you should not see any applications.
