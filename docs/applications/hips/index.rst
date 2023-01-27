.. px-app:: hips

#######################
hips — HiPS tile server
#######################

Serves HiPS_ tiles from an object store backed by Google Cloud Storage.
This is an interim approach that will eventually be replaced by serving the tiles directly from Google Cloud Storage with special code to handle authentication.

.. _HiPS: https://www.ivoa.net/documents/HiPS/

It is a replacement for the normal static file server approach to serving HiPS file trees, used because Rubin Observatory prefers object storage for all data products.

The HiPS list, which catalogues all available HiPS file trees, is generated and served by :px-app:`datalinker` instead of this application.

.. jinja:: hips
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 1

   values
