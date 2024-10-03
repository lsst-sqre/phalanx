#############################
Add new OpenID Connect client
#############################

Gafaelfawr can also serve as an OpenID Connect server, allowing third-party applications running inside Phalanx and OpenID Connect clients outside of Phalanx environments to authenticate users in the same way that the Science Platform does.

Each OpenID Connect client of Gafaelfawr must be pre-registered and assigned a ``client_id`` and password.
To complete an authentication, the client must authenticate with that ``client_id`` and password.
See `the Gafaelfawr documentation <https://gafaelfawr.lsst.io/user-guide/openid-connect.html>`__.

This page describes how to register a new client of Gafaelfawr.
You will need the following information:

* The Phalanx environment to which you'll be adding the new client.
* A short, human-readable name of the new client you're adding.
* The return URL to which the user will be sent after authentication.

.. note::

   The instructions here are specific to SQuaRE-managed Phalanx environments.
   For other environments, you can update the ``oidc-server-secrets`` Gafaelfawr secret key however you maintain static secrets.

Add secret
==========

OpenID Connect clients are configured in the ``oidc-server-secrets`` key of the ``gafaelfawr`` secret.
The value of this key is, unfortunately, a JSON representation of all of the clients.
We currently maintain two parallel records of the clients, one in a structured 1Password secret that is not currently used, and separately in the ``gafaelfawr`` secret.
The goal is to eventually add automation to Phalanx to generate the latter from the former.

#. Open 1Password.
   Go to the 1Password vault for static secrets for the Phalanx environment where you want to add an OpenID Connect client.

#. Create or edit an item named ``oidc-clients``.
   If it doesn't already exist, create it as an item of type :menuselection:`Server`.

#. Add a new section for the new client.
   Set the section title to a short, human-readable name for the OpenID Connect client.
   This name should be enough to tell someone looking at this secret what this client is used for.

#. Add a text field to the new section.
   Change the label to ``id``.
   Change the contents to :samp:`{random-id}.clients.{fqdn}` where the random ID is the results of ``os.urandom(16).hex()`` in Python and the FQDN is the FQDN of the environment.
   For example, ``de5dd2c1fbf648e11d50b6cf3aa72277.clients.data.lsst.cloud``.

#. Add a password field to the new section, changing the label as ``secret``.
   You can let 1Password generate a random 20-character password if you want, or generate one of equivalent entropy however you choose.

#. Add a final text field to the new section.
   Change the label to ``return_uri``.
   Set the value to the return URL of the client.
   This should be provided by the OpenID Connect client and will be the URL to which the user is sent after authentication.

#. Now, you will need to copy this data into the ``gafaelfawr`` secret under the ``oidc-server-secrets`` key, creating that key if it doesn't already exist.
   Unfortunately, you currently have to construct the JSON by hand.
   The value of this key should be a JSON-encoded list of objects, and each object should have keys ``id``, ``secret``, and ``return_uri`` with the information above.
   Be sure to include all the clients, not just the new one that you're adding.

Share the secret with the client
================================

You now need to convey the ``client_id`` (the ``id`` value above) and the ``client_secret`` (the ``secret`` value above) to the OpenID Connect client.
They will need to configure their client software to use that ``client_id`` and ``client_secret`` whenever performing an OpenID Connect authentication.

The easiest way to do this is often to create a separate 1Password secret and share it with the client.

.. warning::

   **DO NOT SHARE THE SECRETS CREATED ABOVE.**
   The client should not have access to the ``oidc-clients`` or ``gafaelfawr`` secrets.

#. Go to the SQuaRE vault and create a new secret.
   Use a name like ``Gafaelfawr <client> OIDC``, replacing ``<client>`` with a *short* human-readable name for the client.
   Use the :menuselection:`Server` item type.

#. Add the information above.
   It's best to call the fields ``client_id``, ``client_secret``, and ``return_uri``, since those are the field names in the OpenID Connect standard and therefore what is usually used in software documentation.
   Enter the same information as above.

When sharing with someone who is managing multiple related clients, feel free to put all of the secrets in the same 1Password item in separate sections.

Now, you can create a one-time 1Password link for this secret and share it with the user in Slack or via email.

Configure Gafaelfawr
====================

If this is the first OpenID Connect client for Gafaelfawr, you will need to enable OpenID Connect server support.
Do this by setting ``config.oidcServer.enabled`` to true in the Gafaelfawr :file:`values-{environment}.yaml` file.
See `the Gafaelfawr documentation <https://gafaelfawr.lsst.io/user-guide/openid-connect.html>`__ for more details.

If the purpose of this OpenID Connect client is to provide services to an IDAC or another external client that may need data rights information (see :dmtn:`253`), ensure the configuration of the Gafaelfawr OpenID Connect server is correct and has a ``dataRightsMapping`` setting.
See `the Gafaelfawr documentation <https://gafaelfawr.lsst.io/user-guide/helm.html#openid-connect-server>`__ for more information.

Then, whether or not you needed to make configuration changes, you will need to sync secrets for this environment.
Follow the normal process (:doc:`/admin/sync-secrets`) to do that.

Finally, you will need to restart Gafaelfawr to pick up the new secret.
Do this by selecting :menuselection:`Restart` on the deployment in Argo CD (see :ref:`branch-deploy-restart`).

.. note::

   Since this requires a Gafaelfawr restart, and since you are changing a secret that contains manually-formatted JSON that is prone to syntax errors that will prevent Gafaelfawr from starting, you will normally want to do this during a maintenance window for a production environment.
