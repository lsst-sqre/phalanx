.. px-app-bootstrap:: nublado

#####################
Bootstrapping Nublado
#####################

For details on how to write the Nublado configuration, see the `Nublado administrator documentation <https://nublado.lsst.io/admin/>`__.

GKE deployments
===============

When deploying Nublado on Google Kubernetes Engine, using Google Artifact Registry as the image source is strongly recommended.
This will result in better image selection menus, allow use of container streaming for faster start-up times, and avoid the need to maintain a pull secret.

For setup instructions for using GAR with Nublado, see `Set up Google Artifact Registry in the Nublado documentation <https://nublado.lsst.io/admin/setup-gar.htl>`__.
For more details about the benefits of using GAR, see the `relevant Nublado documentation page <https://nublado.lsst.io/admin/gar.html>`__.

Telescope and Site deployments
==============================

Image cycles
------------

Telescope and Site deployments have to limit the available images to only images that implement the current XML API.
This is done with a cycle restriction on which images are eligible for spawning.
Failing to set the cycle correctly can cause serious issues with the instrument control plane.

For details on how to configure the cycle, see `image cycles in the Nublado documentation <https://nublado.lsst.io/admin/config/images.html#image-cycles>`__.

Networking
----------

For Telescope and Site deployments that require instrument control, make sure you have any Multus network definitions you need in the :file:`values-{environment}.yaml`.
This will look something like:

.. code-block:: yaml

    singleuser:
      extraAnnotations:
        k8s.v1.cni.cncf.io/networks: "kube-system/dds"

It's possible to list multiple Multus network names separated by commas in the annotation string.
Experimentally, it appears that the interfaces will appear in the order specified.
