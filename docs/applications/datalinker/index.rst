.. px-app:: datalinker

##################################
datalinker — IVOA DataLink service
##################################

datalinker is used to retrieve images referenced in the results of an ObsTAP search.
It does this by returning a DataLink response for the image that includes a signed URL, allowing direct image download from the underlying data store.
Included in that response are service descriptors for any related services for acting on that image.

Currently, datalinker also provides several small redirect-only services to run TAP queries.
These are referenced in DataLink descriptors added to TAP results by the TAP service, and are used by clients to perform related TAP queries for a row of TAP results.
These services will eventually be moved into a separate service.

.. jinja:: datalinker
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 1

   values
