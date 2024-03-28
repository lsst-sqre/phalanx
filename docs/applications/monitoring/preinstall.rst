######################
Pre-Installation Setup
######################

Monitoring has a lot of secrets to communicate with various Phalanx
components and to stock its mapping of alerts (via Slack webhooks) to
channels.

Initial Gafaelfawr Setup
------------------------
Gafaelfawr must have ``config.oidcServer.enabled`` set to ``true`` if you intend to use it as the authentication source for Chronograf.


Initial Secret Setup
--------------------

Do an initial sync of the secrets:

If there is no ``monitoring`` secret in the environment you're working on, create it: :doc:`/admin/add-new-secret`.  Follow the guide at :doc:`/admin/update-a-secret` to add values for ``admin-token`` and ``admin-password``.
I usually use the output from ``openssl rand -hex 16`` to generate a 32-character password representing 16 random bytes, but any random password generation method would do.
* Configure the ``webhooks.yaml`` secret.  If you can, you should probably just copy it from a working environment and edit to suit.  But if you must recreate it from scratch:
* It is a YAML document that is a list of mappings of Slack webooks to channels.

   * Each entry in the list has four string fields: ``channel``, ``phalanx_env``, ``phalanx_host``, and ``webhook_url``.
   * For each channel you want to send alerts to (in the LSSTC slack, they start with ``#status-``), configure as many of these as you can.

      * For a phalanx environment, you should have all four fields.  For instance, at the time of writing, channel ``#status-usdf-rsp-dev`` has ``phalanx_env`` ``usdfdev``, ``phalanx_host`` ``usdf-rsp-dev.slac.stanford.edu``, and a ``webhook_url`` found in the ``Monitoring (InfluxDBv2)`` Slack application in the ``LSSTC`` workspace).
      * It is possible that there are status channels you want to use that are not tied to a specific Phalanx environment (e.g. old Roundtable at ``#status-roundtable``) or which are not specific to a unique instance (e.g. ``#status-square-dev``); in that case, the inapplicable values should be set to the empty string.

   * Once you have the YAML written, base64-encode it, and store the resulting string as the value of ``webhooks.yaml``.

* Create dummy entries for ``influx-alert-token`` and ``telegraf-token``.  These will get overwritten after installation, so their values don't matter.  The telegraf token is not actually used by the ``monitoring`` application, but having it stored safely will make configuring the monitoring agents much easier.
* Audit the secrets: :doc:`/admin/audit-secrets`.  If you are only missing the ``monitoring`` secrets, you're doing fine.  If anything else is incorrect, fix that first before coming back here.
* Sync the secrets: :doc:`/admin/sync-secrets`.

Add the OIDC Secrets to Gafaelfawr
----------------------------------

* Now you'll need the values for ``GENERIC_CLIENT_ID`` and ``GENERIC_CLIENT_SECRET``.  ``GENERIC_CLIENT_ID`` is ``chronograf-client-id`` unless you've done a per-environment override.
* These can be found with ``vault kv get secret/phalanx/<environment>/monitoring``.  They are not in 1Password because they are randomly generated when secrets are synced.
* Add these values to the JSON document inside the ``oidc-server-secrets`` entry of the ``gafaelfawr`` secret, replacing an old entry if needed.

   * ``id`` will be the value of ``GENERIC_CLIENT_ID``.
   * ``return_uri`` will be ``https://<environment FQDN>/chronograf/oauth/OIDC/callback``.
   * ``secret`` will be the value of ``GENERIC_CLIENT_SECRET``.

* Restart Gafaelfawr to pick up the changed secrets.
