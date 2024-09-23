.. px-app:: sia

######################################
sia — Simple Image Access (v2) service
######################################

``sia`` is an image-access API complying with the IVOA SIA (v2) specification.
This application is designed to interact with Butler repositories, through the dax_obscore package https://github.com/lsst-dm/dax_obscore and allows users to find image links for objects that match one or more filter criteria, listed in the IVOA SIA specification https://www.ivoa.net/documents/SIA/.

In our expected use case with the RSP queries in most cases will return results as Datalink_ records which requires an extra hop to fetch the image file.
The SIA service will have as client the RSP Portal Aspect but can also be accessed by other IVOA-compatible clients.

If the SIA application does not appear under a VO Registry, use of it by IVOA-compatible clients will require users to input the SIA service URL manually.

Both POST & GET methods are implemented for the /query API, and any exceptions are intercepted and displayed as a VOTable error in accordance to the specification.


.. jinja:: sia
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 1

   values
