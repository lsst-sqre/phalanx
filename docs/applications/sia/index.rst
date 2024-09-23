.. px-app:: sia

######################################
sia — Simple Image Access (v2) service
######################################

``sia`` is an image-access API complying with the IVOA SIA (v2) specification.
This application is designed to interact with Butler repositories, through the dax_obscore package https://github.com/lsst-dm/dax_obscore and allows users to find image links for objects that match one or more filter criteria, listed in the IVOA SIA specification https://www.ivoa.net/documents/SIA/.

Results of an SIAv2 query will be contain either a datalink if the images are stored behind an authenticated store, or a direct link to the images.

The SIA service will have as client the RSP Portal Aspect but can also be accessed by other IVOA-compatible clients.

If the SIA application does not appear under a VO Registry, use of it by IVOA-compatible clients will require users to input the SIA service URL manually.

Both POST & GET methods are implemented for the /query API, as well as the VOSI-availability and VOSI-capabilities endpoints.


.. jinja:: sia
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 1

   values
