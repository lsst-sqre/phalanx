.. _changing-the-admin-password:

###########################
Changing the Admin Password
###########################

If you need to change the non-auth-proxy-created server admin user's password, you need to change it in the database and in the Phalanx configuration, in that order.

#. Come up with a new password.
#. Shell into the running Grafana pod:

   .. code-block:: shell

      kubectl --context <some phalanx env> --namespace grafana exec -it <grafana pod name> --container grafana -- /bin/bash

#. Run this command to change the password:

   .. code-block:: shell

      grafana cli admin reset-admin-password

#. Update the ``grafana-admin-password`` Phalanx secret.
#. Restart the Grafana instance deployment.
#. Maybe wait 5 minutes for the admin user lock-out to expire.

But Why??
=========

Changing the password in the Helm/Phalanx configuration will not actually change the password in the database.
You need to use the Grafana CLI for that.
The Grafana CLI change password functionality works by starting a completely separate instance of Grafana.
It uses the admin credentials in environment variables that are in that container from the Helm/Phalanx configuration.
If you change those environment variables first, then the CLI will not be able to auth to make the actual database password change

BUT: The Grafana helm chart uses some sidecar containers that talk directly to the Grafana instance to keep the CRD-based resources in sync.
These use the admin creds in the environment. These need to be updated after the password is changed in the database.

BUT: During the time between when the password is updated in the database and when the password is updated in the Helm/Phalanx config, these sidecar containers will be using the old password, and the admin user may get locked out.
