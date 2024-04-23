###############################
Configuring /tmp in a container
###############################

The ``web-service`` starter creates a deployment with an entirely read-only file system.
This is ideal for security, since it denies an attacker the ability to create new local files, which makes some attacks harder.

Some applications, however, need working scratch space.
For those applications, you may need to mount a writable :file:`/tmp` file system.
Here is how to do that:

#. Add a ``volumes`` section to the ``spec`` part of the Deployment_ (or add a new element one is not already there) that creates a volume for temporary files:

   .. code-block:: yaml
      :caption: deployment.yaml

      volumes:
        - name: "tmp"
          emptyDir: {}

#. Mount that volume by adding a ``volumeMounts`` section to the main container in the Deployment_ (or add it to the volume mounts if there already are others):

   .. code-block:: yaml
      :caption: deployment.yaml

      volumeMounts:
        - name: "tmp"
          mountPath: "/tmp"

.. warning::

   Files written to this temporary directory are stored in `node ephemeral storage <https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#configurations-for-local-ephemeral-storage>`__, which is shared between all pods running on that node.
   Writing excessive amounts of data to this directory may exhaust node resources and cause problems for other applications in the cluster.

   This type of temporary directory should therefore only be used for small files.
   Applications that need large amounts of temporary space should allocate and mount a `persistent volume`_ instead.
