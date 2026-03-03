##################
Temporary instance
##################

When doing some kinds of maintenance on the cluster that a `Vault`_ instance is provisioned in, like a full cluster rebuild, there needs to be a vault instance accessible outside of the cluster.
For `Google Kubernetes Engine`_ (GKE) clusters that use `Google Cloud Storage`_ (GCS) as a backend and `Google Cloud Key Management`_ (GCKM) for sealing, we can quickly provision and destroy a Vault instance using a copy of the existing storage.

.. caution::

   This is only useful for read-only use cases for the temp Vault instance.
   No changes to the Vault storage will persist using the following steps.

You can use the `vault-temp repo <https://github.com/lsst-sqre/vault-temp>`__ to do this for the ``roundtable-prod`` and ``roundtable-dev`` clusters. Clone that repo and follow the instructions in the ``README.md``.
