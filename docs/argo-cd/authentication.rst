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

#. On the GCP console, go to "OAuth consent screen" under "APIs & Services."

#. Select "Internal" and click Create.

#. Enter the environment information.
   For example (adjust for the environment):
   - App name: Rubin Science Platform (int)
   - User support email: Choose the address of the person doing this
   - Application home page: https://data-int.lsst.cloud/
   - Authorized domains: lsst.cloud
   - Developer contact information email addresses: Work email address

#. Click "Save and Continue."

#. Add the ``openid`` scope and click "Save and Continue."

#. Click "Back to Dashboard."

#. Go to "Credentials" still under "APIs & Services."

#. Click "Create Credentials" and choose "OAuth client ID."

#. Choose "Web application" as the application type.

#. Enter "Argo CD" as the name.

#. Add the ``/argo-cd/api/dex/callback`` route under "Authorized redirect URIs."
   For example: https://data-int.lsst.cloud/argo-cd/api/dex/callback

#. Click on create.
   This will pop up a dialog with the client ID and secret for the newly-created OAuth client.

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

#. Using ``kubectl``, edit ``secret/argocd-secret`` in the ``argocd`` namespace and add a key named ``dex.clientSecret`` whose contents is the base64-encoded client secret from the GCP console dialog pop-up.
   Be sure when base64-encoding that value to not include a trailing newline.

#. Create a PR with the above changes, merge it, and then sync Argo CD.
   Ensure that both the ``argocd-server`` and ``argocd-dex-server`` deployments are restarted (in case the Argo CD Helm chart doesn't ensure this).

#. Go to the ``/argo-cd`` route on the environment.
   Log out if you're logged in with the admin password.
   You should see a login in with Google option appear.
   Click on it and you should be able to authenticate with Google.
   Anyone in the same hosted domain can authenticate, but if you aren't one of the listed users, you should not see any applications.
