################################
Creating a Sasquatch write token
################################

Write access to the Sasquatch metrics service is controlled, via Gafaelfawr_, by the ``write:sasquatch`` scope.
Any process that needs to write metrics to Sasquatch therefore must authenticate with a Gafaelfawr token for the Phalanx environment in which the Sasquatch it is writing to is running.

For individual use, this can be a normal user token.
Automated processes, such as Jenkins jobs, should instead use a service token.
This document describes how to create one using the Gafaelfawr API.

Only administrators of the Phalanx environment (users with ``admin:token`` scope) can follow this procedure.

#. Create a user token for yourself with ``admin:token`` scope in the same Phalanx environment as the Sasquatch instance the service account will be connecting to.
   To do this, go to :menuselection:`Security tokens` in the pull-down menu at the top right of the front page of the Phalanx environment.
   Then, click on the :guilabel:`Create token` button.
   Be sure to select the ``admin:token`` scope for the resulting user token.
   Store the token you receive somewhere secure, such as your 1Password vault.

   This first step only has to be done once.
   The created token can be reused if you need to create more service tokens.

#. Choose the username for the service token.
   This must begin with ``bot-`` and follow our normal username restrictions (see :dmtn:`225`).

#. From a system with cURL installed, run the following command:

   .. code-block:: sh

      curl -H 'Authorization: bearer <admin-token>' \
           --json '{"username": "<username>", "name": "<description>", "token_type": "service", "scopes": ["write:sasquatch"]}' \
           https://<environment>/auth/api/v1/tokens

   Replace ``<username>`` with the chosen username, ``<description>`` with a short human-readable description of the service that will be using this token, and ``<environment>`` with the URL of the Phalanx environment.

#. Retrieve the token from the value of the ``token`` key in the resulting JSON.
   This is the secure (password-equivalent) token that will be used by the service to send data to Sasquatch.

#. Configure the service that is posting metrics to Sasquatch to include an authorization header in that request.
   The header should be ``Authorization: bearer <token>``, where ``<token>`` is the token created in the previous steps.
