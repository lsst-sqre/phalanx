.. px-app:: datalinker

##################################
datalinker — IVOA DataLink service
##################################

datalinker provides various facilities for discovering and referring to data products and services within the Rubin Science Platform.
It is primarily based on the IVOA DataLink standard, but also provides some related service discovery facilities beyond the scope of that standard.

Most significantly, datalinker is used to retrieve images referenced in the results of an ObsTAP search.
It does this by returning a DataLink response for the image that includes a signed URL, allowing direct image download from the underlying data store.

It also provides the HiPS list service, which collects the property files of HiPS data sets served by :px-app:`hips` and returns them with appropriate URLs, and implements a variety of "microservice" endpoints that rewrite simple service-descriptor-friendly APIs into redirects to other RSP services.

.. jinja:: datalinker
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 1

   values
