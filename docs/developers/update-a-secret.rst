######################
Add or update a secret
######################

Adding or updating a secret for your application requires changing Vault, which must be done by the environment administrator.
However, there are some steps that you, as the application developer, should take first:

#. If you are adding a new secret, update :file:`secrets.yaml` or :file:`secrets-{environment}.yaml` for that application with the details of the new secret.
   See :doc:`secrets-spec` for details about the format of that file.

#. If necessary, update the application templates to pass in the new secrets to your application.
   See :ref:`dev-inject-secrets`.

#. Determine the values of any new static secrets for every environment in which your application is deployed that will need the new secret.

Once you have done those steps on a PR branch, contact the environment administrator for each Phalanx environment where a secret needs to be added or updated.
Provide them with the new static secret values and ask them to create or update the secrets.

The environment administrator will then follow the instructions in either:

- :doc:`/admin/add-new-secret`
- :doc:`/admin/update-a-secret`
