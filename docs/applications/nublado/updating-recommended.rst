############################################
Update the recommended Notebook Aspect image
############################################

The ``recommended`` tag for JupyterLab images is usually a recent weekly image.
The image tagged ``recommended`` is guaranteed by SQuaRE to be compatible with other services and materials, such as tutorial or system testing notebooks, that we make available on RSP deployments.

This document explains the process for moving the ``recommended`` tag.
It also documents how to make an image that is *not* tagged ``recommended`` the default image, which is sometimes required, particularly in Telescope and Site environments.

Tagging a new container version
--------------------------------

When a new version has been approved (after passing through its prior QA and sign-off gates), the ``recommended`` tag must be updated to point to the new version.
To do this, run the GitHub retag workflow for https://github.com/lsst-sqre/sciplat-lab repository as follows:

#. Go to `the retag workflow page <https://github.com/lsst-sqre/sciplat-lab/actions/workflows/retag.yaml>`__.
#. Click :guilabel:`Run workflow`.
#. Enter the tag of the image to promote to recommended under :guilabel:`Docker tag of input container`.
   This will be a tag like ``w_2023_40``.
#. Enter ``recommended`` under :guilabel:`Additional value to tag container with`.
#. Do not change the field :guilabel:`fully-qualified URI for output Docker image`.
#. Click the :guilabel:`Run workflow` submit button.

.. _different-default:

Changing the environment default image to some tag other than "recommended"
---------------------------------------------------------------------------

Tags are global per container image repository (that is, ``docker.io/sciplat-lab:recommended``, for instance, refers to the same image in all environments).
It is quite often the case that Telescope and Site, in particular, needs the image that is recommended by default for a given environment to vary, because their environments may not be running the same XML cycle.

To change the default image to a new tag, you must do the following.

#. Locate the JupyterLab Controller configuration for the environment you're working with.
   This will be in the Phalanx GitHub repository at ``/applications/nublado/`` and will be the :file:`values-{environment}.yaml` file there.
   In that file, you should find the key ``controller.config.images.recommendedTag``.
   If you do not find it, then that environment is currently using ``recommended`` as its default image.

#. Set this key (creating it if necessary) to whatever string represents the correct recommended-by-default image for that instance.
   For instance, for a Telescope and Site environment, this will likely look something like ``recommended_c0032``.

#. Create a pull request against https://github.com/lsst-sqre/phalanx that updates this setting.

#. Once this change is merged, sync the nublado application (using Argo CD) in the affected environments.

You do not have to wait for a maintenance window to do this, since the change is low risk.
It will, however, result in a very brief outage for Notebook Aspect lab spawning while the JupyterLab Controller is restarted.
