######################
Argo CD authentication
######################

Argo CD supports three main methods of authentication: the ``admin`` account, local accounts, or SSO (Single Sign-On).
We use the ``admin`` account plus SSO.

Argo CD documentation recommends disabling the ``admin`` account once user access via SSO is configured.
We've chosen to ignore that advice in favor of having an easy and reliable emergency access mechanism that doesn't rely on any other service, and have instead created strong, randomized ``admin`` passwords.
Still, normal Argo CD access should be done via SSO, both to minimize use of the ``admin`` password and for attribution of actions taken via the web UI.

On :abbr:`IDF (Interim Data Facility)` installations, Argo CD is configured to use Google OAuth for SSO using the same Google Cloud Identity domain as is used for other IDF operations.
On all other installations, Argo CD is configured to use GitHub.

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

#. For SQuaRE-run enviroments, go to the RSP-Vault 1Password vault and create a new Login item with a name like "Argo CD Google OAuth - data-int.lsst.cloud" (replacing the last part with the FQDN of the environment).
   In this secret, put the client ID in the username field.
   Put the secret in the password field.
   Create a field labeled ``generate_secrets_key`` with value ``argocd dex.clientSecret``.
   Create a field labeled ``environment`` with value ``data-int.lsst.cloud`` (replace with the FQDN of the environment).
   Save this 1Password secret.

#. If the environment already exists, get a Vault write token for the environment (or the Vault admin token) and set the ``dex.clientSecret`` key in the ``argocd`` secret in the Vault path for that environment (something like ``secret/k8s_operator/data-int.lsst.cloud``, replacing the last part with the FQDN of the environment).
   This will add the value to the Argo CD secret once vault-secrets-operator notices the change.
   You can delete ``argocd-secret`` to immediately recreate it to speed up the propagation.

#. In the Phalanx repository, under ``services/argocd``, edit the ``values-*.yaml`` file for the relevant environment.
   In ``argo-cd.server.config``, at the same level as ``helm.repositories``, add the following, modifying the URLs and ``hostedDomains`` for the environment and changing the ``clientID`` to the value from the pop-up:

   .. code-block:: yaml

      url: https://data-int.lsst.cloud/argo-cd
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

#. In the same file, add a new ``argo-cd.server.rbacConfig`` key as follows:

   .. code-block:: yaml

      rbacConfig:
        policy.csv: |
          g, adam@lsst.cloud, role:admin
          g, afausti@lsst.cloud, role:admin
          g, christine@lsst.cloud, role:admin
          g, frossie@lsst.cloud, role:admin
          g, jsick@lsst.cloud, role:admin
          g, krughoff@lsst.cloud, role:admin
          g, rra@lsst.cloud, role:admin
        scopes: "[email]"

   Change the list of users to the email addresses of the users who should have admin access to this environment.

#. If the environment already exists, create a PR with the above changes, merge it, and then sync Argo CD.
   Ensure that both the ``argocd-server`` and ``argocd-dex-server`` deployments are restarted (in case the Argo CD Helm chart doesn't ensure this).

#. Go to the ``/argo-cd`` route on the environment.
   Log out if you're logged in with the admin password.
   You should see a login in with Google option appear.
   Click on it and you should be able to authenticate with Google.
   Anyone in the same hosted domain can authenticate, but if you aren't one of the listed users, you should not see any applications.

Configuring GitHub SSO
======================

To set up Google SSO authentication to Argo CD in a new cluster, take the following steps:

#. From the GitHub page of the organization in which you want to create the OAuth application (such as `lsst-sqre <https://github.com/lsst-sqre>`__), go to :guilabel:`Settings → Developer Settings → OAuth Apps`.

#. Click :guilabel:`New OAuth App`.

#. Enter the following information (adjust for the environment):
   - Application name: ``RSP Argo CD (IDF-int)``
   - Homepage URL: ``https://data-int.lsst.cloud/argo-cd``
   - Authorization callback URL: ``https://data-int.lsst.cloud/argo-cd/api/dex/callback``

#. Click :guilabel:`Register Application`.

#. Click :guilabel:`Generate a new client secret`.

#. For SQuaRE-run enviroments, go to the RSP-Vault 1Password vault and create a new Login item with a name like "Argo CD GitHub OAuth - data-int.lsst.cloud" (replacing the last part with the FQDN of the environment).
   In this secret, put the client ID in the username field.
   Put the client secret in the password field.
   Create a field labeled ``generate_secrets_key`` with value ``argocd dex.clientSecret``.
   Create a field labeled ``environment`` with value ``data-int.lsst.cloud`` (replace with the FQDN of the environment).
   Save this 1Password secret.

#. If the environment already exists, get a Vault write token for the environment (or the Vault admin token) and set the ``dex.clientSecret`` key in the ``argocd`` secret in the Vault path for that environment (something like ``secret/k8s_operator/data-int.lsst.cloud``, replacing the last part with the FQDN of the environment).
   Be sure to use ``vault kv patch`` to add the key to the existing secret.
   This will add the value to the Argo CD secret once vault-secrets-operator notices the change.
   You can delete ``argocd-secret`` to immediately recreate it to speed up the propagation.

#. In the Phalanx repository, under ``services/argocd``, edit the ``values-*.yaml`` file for the relevant environment.
   In ``argo-cd.server.config``, at the same level as ``helm.repositories``, add the following, modifying the URL for the environment and changing the ``clientID`` to the value from GitHub:

   .. code-block:: yaml

      url: https://data-int.lsst.cloud/argo-cd
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

#. In the same file, add a new ``argo-cd.server.rbacConfig`` key as follows:

   .. code-block:: yaml

      rbacConfig:
        policy.csv: |
          g, lsst-sqre:square, role:admin

   Add lines for additional GitHub teams as needed for that environment.
   Be aware that this uses the human-readable name of the team (with capital letters and spaces if applicable), not the slug.

#. If the environment already exists, create a PR with the above changes, merge it, and then sync Argo CD.
   Ensure that both the ``argocd-server`` and ``argocd-dex-server`` deployments are restarted (in case the Argo CD Helm chart doesn't ensure this).

#. Go to the ``/argo-cd`` route on the environment.
   Log out if you're logged in with the admin password.
   You should see a login in with Google option appear.
   Click on it and you should be able to authenticate with Google.
   Anyone in the same hosted domain can authenticate, but if you aren't one of the listed users, you should not see any applications.
