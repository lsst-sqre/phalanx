################
Configuring mobu
################

Configuring mobu consists primarily of defining the flocks of monkeys that it should run.
This is done by setting the ``autostart`` key in the ``values-*.yaml`` file for that deployment to a list of flock definitions.
The definition of a flock must follow the same schema as a ``PUT`` to the ``/mobu/flocks`` route to create a new flock via the API.
Complete documentation is therefore available at the ``/mobu/redoc`` route on a given deployment.
This is just an overview of the most common configurations.

Simple configuration
====================

Here is a simple configuration with a single flock that tests the Notebook Aspect by spawning a pod, running some Python, and then destroying the pod again:

.. code-block:: yaml

   autostart:
     - name: "python"
       count: 1
       users:
         - username: "bot-mobu-user"
       scopes: ["exec:notebook"]
       business:
         type: "JupyterPythonLoop"
         restart: true
         options:
           max_executions: 1
           code: "print(1+1)"

Important points to note here:

* The ``autostart`` key takes a list of flocks of monkeys.
  Each one must have a ``name`` (which controls the URL for that flock under ``/mobu/flocks`` once it has been created) and a ``count`` key specifying how many monkeys will be performing this test.

* Users must be defined for each monkey.
  There are two ways to do this: specifying a list of users equal to the number of monkeys being run, or providing a specification for users that is used to programmatically generate usernames, UIDs, and GIDs.
  An example of the latter will be given below.
  Here, this specifies a single user with the name ``bot-mobu-user``.
  Usernames must begin with ``bot-``.
  Neither a UID nor a GID is specified, which means that Gafaelfawr has to be ble to generate UIDs and GIDs on the fly.
  This configuration will therefore only work if this deployment enables Firestore for UID and GID generation, and enables synthesizing user private groups.

* If the monkey user will need additional scopes, they must be specified.
  Here, the required scope is ``exec:notebook``, which allows spawning Notebooks.
  More scopes would be needed if the monkey were running notebooks that interacted with other applications.

* The ``business.type`` key specifies the type of test to perform.
  Here, ``JupyterPythonLoop`` just runs a small bit of Python through the Jupyter lab API after spawning a lab pod.
  ``options.code`` can be used to specify the Python code to be run in the loop.
  See the full mobu documentation for more details.

* ``restart: true`` tells mobu to shut down and respawn the pod if there is any failure.
  The default is to attempt to keep using the same pod despite the failure.

Testing with notebooks
======================

Here is a more complex example that runs a set of notebooks as a test:

.. code-block:: yaml

   autostart:
     - name: "firefighter"
       count: 1
       users:
         - username: "bot-mobu-recommended"
           uidnumber: 74768
           gidnumber: 74768
       scopes:
         - "exec:notebook"
         - "exec:portal"
         - "read:image"
         - "read:tap"
       business:
         type: "NotebookRunner"
         options:
           repo_url: "https://github.com/lsst-sqre/system-test.git"
           repo_branch: "prod"
           max_executions: 1
         restart: true

Here, note that the UID and primary GID for the user are specified, so this example will work in deployments that do not use Firestore and synthesized user private groups.

This uses the business ``NotebookRunner`` instead, which checks out a Git repository and runs all notebooks at the top level of that repository.
The repository URL and branch are configured in ``options``.
``options.max_executions: 1`` tells mobu to shut down and respawn the pod after each notebook.
This exercises pod spawning more frequently, but does not test the lab's ability to run a long series of notebooks.
One may wish to run multiple flocks in a given environment with different configurations for ``max_executions``.
These notebooks need more scopes, so those scopes are specified.

Here is a different example that runs multiple monkeys in a flock:

.. code-block:: yaml

   autostart:
     - name: "firefighter"
       count: 5
       user_spec:
         username_prefix: "bot-mobu-recommended"
         uid_start: 74768
         gid_start: 74768
       scopes:
         - "exec:notebook"
         - "exec:portal"
         - "read:image"
         - "read:tap"
       business:
         type: "NotebookRunner"
         options:
           repo_url: "https://github.com/lsst-sqre/system-test.git"
           repo_branch: "prod"
           max_executions: 1
         restart: true

This is almost identical except that it specifies five monkeys and provides a specification for creating the users instead of specifying each user.
The users will be assigned consecutive UIDs and GIDs starting with the specified ``uid_start`` and ``gid_start``.
The usernames will be formed by adding consecutive digits to the end of the ``username_prefix``.

Testing TAP
===========

Here is an example of testing the TAP application:

.. code-block:: yaml

   autostart:
     - name: "tap"
       count: 1
       users:
         - username: "bot-mobu-tap"
           uidnumber: 74775
           gidnumber: 74775
       scopes: ["read:tap"]
       business:
         type: "TAPQueryRunner"
         restart: true
         options:
           sync: true
           query_set: "dp0.2"

Note that ``business.type`` is set to ``TAPQueryRunner`` instead.
``options.sync`` can choosen between sync and async queries, and ``options.query_set`` can be used to specify the query set to run.
