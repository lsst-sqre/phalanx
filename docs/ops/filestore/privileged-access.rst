##################################
Privileged access to the filestore
##################################

Currently, we do not have any way to make containers with privileged
filesystem access available from JupyterHub.

In order to get privileged access to the filestore, you will need access
to ``kubectl`` with admin privileges to the cluster you want to work on.

Save the following file as ``copier.yaml``; you may need to edit it to
point to the correct filestore, and of course if you need multiple
filestores present (for instance, for copying data between environments)
then you will need to create multiple Volume/VolumeMount pairs so
multiple filestores are presented within the container.

.. code-block:: yaml

    apiVersion: v1
    kind: Pod
    metadata:
      name: copier
      namespace: copier
    spec:
      containers:
      - name: main
	image: ubuntu:latest
	args: [ "tail", "-f", "/dev/null" ]
	volumeMounts:
	- mountPath: /mnt
	  name: share
      volumes:
      - name: share
	nfs:
	  path: /share1
	  server: 10.13.105.122
	  # 10.87.86.26 is IDF dev
	  # 10.22.240.130 is IDF int
	  # 10.13.105.122 is IDF prod

In order to spin up this pod, do the following:

  * ``kubectl create ns copier``
  * ``kubectl apply -f copier.yaml``
  * ``kubectl exec -it -n copier copier -- /bin/bash -l``

Once you do that, you have a root prompt and the instance filestore is
mounted at ``/mnt``.
With great power comes great responsibility.

When you're done, delete the namespace.  This will also destroy the
privileged pod:

  * ``kubectl delete ns copier``

**Examples:**

  * Get usage data by username, sorted by usage, largest at the bottom:

    ::
    
        du -s -BM /mnt/home/* \
        | sed -e 's/\s\+/,/' \
        | sed -e 's|/mnt/home/||' \
        | sort -nr

  * Make archival copy of user ``foo``'s previous ``.local`` for analysis.

    ::

        tar cvpfz /tmp/foo-local.tgz /home/foo/.local.20210804223021

