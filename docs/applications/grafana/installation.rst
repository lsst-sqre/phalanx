############
Installation
############

Database
========

Grafana requires a SQL database to run. It can use a `Sqlite`_ database stored on its data volume, but:
* It doesn't behave well on networked storage
* It doesn't perform well with a lot of users and dashboards and you'll probably have to migrate off of it anyway
* It doesn't perform well with moderate use of the alerting functionality

For those reasons, this chart only supports using an external database, and it assumes the database already exists.
The database password is taken from the ``database-password`` :ref:`Phalanx secret <static-secrets>`.
The rest of the database connection parameters should be defined in the ``deployment.config.database`` as described in the `Grafana database config docs`_.

.. _Sqlite: https://www.sqlite.org/

CloudSQl On GCP
---------------
If you are running this in a `GCP`_-based Phalanx, you should use a :ref:`Cloud SQL <using-cloud-sql>` database.
This requires an sidecar container that runs the CloudSQL auth proxy.
To configure and enable this auth proxy:

- Set ``cloudsql.enabled`` to ``true``
- Set ``grafana.config.database.host`` to ``"localhost"``

.. _GCP: https://cloud.google.com/
.. _Grafana database config docs: https://grafana.com/docs/grafana/latest/setup-grafana/configure-grafana/#database

Grafana Server Administrator
============================

There is a special kind of Grafana user called a `Grafana server administrator`_, which is the most powerful kind of Grafana user.
At least one user should be a server administrator.

This chart assumes that any requests that make it to the Grafana instance will have already been authed by Gafaelfawr.
It enables the `Grafana auth proxy`_ and configures it to create Grafana users based on the usernames that Gafaelfawr headers that get injected.
It disables the Grafana login page, which makes it impossible to access Grafana in any other way.

This works great, but there is no way to automatically make a Grafana-auth-proxy-created user into a Grafana server administrator. There is a non-auth-proxy-created server admin user though. After this chart is synced for the first time in an environment, you need to go through this manual process to make a proxy-created user into a server administrator, by using the non-proxy-created server admin user:

#. Sync the chart and wait until the Grafana instance is ready.
#. Visit ``https://<base-url>/grafana``, which will create a (non-server-admin) Grafana user for you and log you in.
#. Log out of Grafana.
#. Set ``grafana.authProxy.enabled`` to ``false`` and sync the chart. This will disable the auth proxy and enable the login page
#. Get the non-proxy-created server admin user's password:

       kubectl --context <context for the env you're deploying to> --namespace grafana get secrets/grafana --template='{{ index .data "grafana-admin-password" }}' | base64 -d
#. Get the non-proxy-created server admin user's username from ``grafana.config.admin_user``.
#. Visit ``https://<base-url>/grafana`` and log in using that username/password combo.
#. Follow `these instructions`_ to make your proxy-created user into a server admin.
#. Log out of Grafana.
#. Set ``Grafana.authProxy.enabled`` back to ``false`` and sync the chart.
#. Visit ``https://<base-url>/grafana``. You should now be a server admin!


.. _Grafana auth proxy: https://grafana.com/docs/grafana/latest/setup-grafana/configure-security/configure-authentication/auth-proxy/
.. _Grafana server administrator: https://grafana.com/docs/grafana/latest/administration/roles-and-permissions/#grafana-server-administrators
.. _these instructions: https://grafana.com/docs/grafana/latest/administration/user-management/server-user-management/assign-remove-server-admin-privileges/
