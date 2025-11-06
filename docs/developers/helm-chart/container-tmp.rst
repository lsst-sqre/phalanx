###############################
Configuring /tmp in a container
###############################

The ``web-service`` starter creates a deployment with an entirely read-only file system.
This is ideal for security, since it denies an attacker the ability to create new local files, which makes some attacks harder.

Some applications, however, need working scratch space.
For those applications, you may need to mount a writable :file:`/tmp` file system.
There are two good options for this:

* `Memory-backed emptyDir`_
* `Generic ephemeral volume`_

.. note::

   These recommendations are only for data that doesn't need to be persisted across pod restarts.
   If you need a place to put data that persists even when attached pods disappear, you should use a `persistent volume`_.

.. _Memory backed emptyDir: https://kubernetes.io/docs/concepts/storage/volumes/#emptydir-memory-configuration-example
.. _Generic ephemeral volumes: https://kubernetes.io/docs/concepts/storage/ephemeral-volumes/#generic-ephemeral-volumes

Memory-backed emptyDir
======================

If you only intend to use a small amount of scratch space, consider using a memory-backed ``emptyDir`` volume.
Any files written to this type of volume will be stored in memory, not on any disk.


Here is how to do that:

#. Add a ``volumes`` section to the ``spec`` part of the Deployment_ (or add a new element if one is not already there) that creates a volume for temporary files:

   .. code-block:: yaml
      :caption: deployment.yaml

      volumes:
        - name: "tmp"
          emptyDir:
            medium: "Memory"
            sizeLimit: "2Mi"

#. Mount that volume by adding a ``volumeMounts`` section to the main container in the Deployment_ (or add it to the volume mounts if there already are others):

   .. code-block:: yaml
      :caption: deployment.yaml

      volumeMounts:
        - name: "tmp"
          mountPath: "/tmp"

.. warning::

   This is only recommended for small usages.
   Files written to this directory count against your container's memory requests and limits.
   If you write more data than your container limit, then the kernel OOM killer will ungracefully kill your pod.
   You can prevent an OOM kill by declaring a ``sizeLimit``.
   Then, your application will see a full disk when that limit is reached, which is probably what you want instead of risking an OOM kill.

Generic ephemeral volume
========================

If you need a lot of scratch space, consider using a generic ephemeral volume.
This provisions an external disk volume using whatever storage class you declare, which will get destroyed when your pod stops or restarts.

Here is how to do that:

#. Add a ``volumes`` section to the ``spec`` part of the Deployment_ (or add a new element if one is not already there) that creates a volume for temporary files:

   .. code-block:: yaml
      :caption: deployment.yaml

      volumes:
        - name: "tmp"
          ephemeral:
            volumeClaimTemplate:
              spec:
                accessModes:
                  - "ReadWriteOnce"
                storageClassName: "standard-rwo"
                resources:
                  requests:
                    storage: "2Gi"

#. Mount that volume by adding a ``volumeMounts`` section to the main container in the Deployment_ (or add it to the volume mounts if there already are others):

   .. code-block:: yaml
      :caption: deployment.yaml

      volumeMounts:
        - name: "tmp"
          mountPath: "/tmp"

You may also need to adjust the security context of your pod to allow writing to that volume by setting ``fsGroup`` in the ``securityContext`` section of the pod spec.

Why not a disk-based emptyDir?
==============================

Files written to this disk-based emptyDirs are stored in `node ephemeral storage <https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#configurations-for-local-ephemeral-storage>`__, which is shared between all pods running on that node.
Writing excessive amounts of data to this directory may exhaust node resources and cause problems for other applications in the cluster.
