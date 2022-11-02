###################
Configuring storage
###################

Gafaelfawr uses Redis for persistent storage.
When deploying Gafaelfawr, you will need to choose between three possible storage configurations based on the needs of the environment.

Ephemeral
=========

For test environments, or for environments where no one is expected to use persistent user tokens, it may be acceptable to invalidate all tokens on each Gafaelfawr restart.
This is the simplest configuration, since it doesn't require persistent volumes.
To choose this method, put:

.. code-block:: yaml

   redis:
     persistence:
       enabled: false

in the ``values-*.yaml`` file for that environment.

.. _dynamic-gafaelfawr:

Dynamic provisioning
====================

The default Gafaelfawr behavior is to use `dynamic provisioning <https://kubernetes.io/docs/concepts/storage/dynamic-provisioning/>`__.
Gafaelfawr will request (via a ``StatefulSet``) a 1GiB volume using the default storage class with access mode ``ReadWriteOnce``.
These values can be overridden with ``redis.persistence.size``, ``redis.persistence.storageClass``, and ``redis.persistence.accessMode``.

On GKE environments, the recommended configuration is to enable the Google Compute Engine Physical Disk CSI driver (this can be done via the GKE cluster configuration) and then use its storage class.
Do this by putting:

.. code-block:: yaml

   redis:
     persistence:
       storageClass: "standard-rwo"

in the ``values-*.yaml`` file for that environment.

You may want to change the reclaim policy from the default.
First, start Gafaelfawr so that hte persistent volume claim and corresponding persistent volume have been created.
Then, locate that persistent volume and change its reclaim policy from the default (usually ``Delete``) to ``Retain``.
This provides some additional protection against wiping the storage in accidents or application redeployments that cause the ``StatefulSet`` and its ``PersistentVolumeClaim`` to be deleted.

Existing ``PersistentVolumeClaim``
==================================

Finally, Gafaelfawr can be configured to use an existing ``PersistentVolumeClaim``.
This is the most flexible approach, since the ``PersistentVolumeClaim`` can be created outside of the Gafaelfawr chart with whatever parameters are desired.

To use this method, add:

.. code-block:: yaml

   redis:
     persistence:
       volumeClaimName: "<volume-claim>"

to ``values-*.yaml`` file for that environment, replacing ``<volume-claim>`` with the name of an existing ``PersistentVolumeClaim`` in the ``gafaelfawr`` namespace.

When using this method, Phalanx does not attempt to create or manage the ``PersistentVolumeClaim`` resource.
This must be done outside of Phalanx.
