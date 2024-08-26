#########################
Portal Volume Definitions
#########################

There are three Portal volumes, ``config``, ``privateWorkarea``, and ``sharedWorkarea``.
Each portal volume is defined in the configuration YAML as an object with keys ``hostPath``, ``nfs``, and ``pvc``.
At most one of these keys must have a non-null value.
If all objects have null values, an ``emptyDir`` is used for this volume.
This is acceptable for ``config`` and ``privateWorkarea`` (with caveats explained below), but if there is more than one replica of the Portal pod, this will not work correctly for ``sharedWorkarea``, as an ``emptyDir`` is not shareable.

----
Keys
----

^^^^^^^^
hostPath
^^^^^^^^

The ``hostPath`` object, if nonempty, has a single key, ``path``, with a string value representing the filesystem path on the host volume.

^^^
nfs
^^^

The ``nfs`` object, if nonempty, has two keys, ``path`` and ``server``.  These each have string values representing the mount path on the NFS server and the DNS name or IP address of the server respectively.

^^^
pvc
^^^

The ``pvc`` object, if nonempty, has two keys, ``size`` and ``storageClass``.  These each have string values representing the size (e.g. ``20Gi``) and Kubernetes ``storageClass`` of the volume.  The storage class must have a provisioner capable of providing the correct access mode.

The storage class mode is constrained by the volume: for ``config`` it must be ``ReadOnlyMany``, for ``privateWorkarea`` it must be ``ReadWriteOnce``, and for ``sharedWorkarea`` it must be ``ReadWriteMany``.
Storage class provisioners that support ``ReadWriteMany`` are extremely unusual, which is why you will very likely end up with ``nfs`` or ``hostPath`` for your ``sharedWorkArea``.

------------------
Individual Volumes
------------------

^^^^^^^^^^^^^^
sharedWorkarea
^^^^^^^^^^^^^^

``sharedWorkarea`` is the most complex.  as explained in :doc:`/applications/portal/bootstrap`.
If you have more than one replica, which you very likely will, each replica will need to reference storage shared between all replicas.
In turn, that very likely means you will require NFS or a ``hostPath`` volume type, since very few storage class provisioners support ``ReadWriteMany``.

^^^^^^
config
^^^^^^

``config`` is more straightforward.
It may either be an ``emptyDir``, which means its storage is allocated from node-local Kubernetes ``ephemeralStorage``, or it may be a shared volume.
It is usually not problematic for ``config`` to come from ``ephemeralStorage`` because is is quite small: a few kilobytes.

^^^^^^^^^^^^^^^
privateWorkarea
^^^^^^^^^^^^^^^

``privateWorkarea`` is conceptually simple: it's storage that is private to a particular Firefly pod.
However, the implementation forces some unusual choices.
Portal is deployed as a ``StatefulSet`` rather than a ``Deployment`` and this is why.
``Deployment`` offers no way to do templated private volumes, but ``StatefulSet`` does.
The ``privateWorkarea`` can be problematic to put on ``ephemeralStorage`` because it can easily grow to dozens of GiB.
On nodes with small attached local disks, which is how ``ephemeralStorage`` is implemented by default, this in turn can lead to resource exhaustion, ``Pod`` eviction, and disappearance of cached images from the spawner menu.
