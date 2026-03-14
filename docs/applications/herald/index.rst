.. px-app:: herald

################################
herald — Alert retrieval service
################################

Herald provides authenticated HTTP access to archived Rubin alert packets stored in the USDF S3 alert archive.
It accepts a single alert ID and returns the corresponding alert packet as either Avro OCF (default), FITS, or JSON.
It also exposes cutout images, the Avro schema, and an IVOA DataLink VOTable endpoint for discovery of related data products.

.. jinja:: herald
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 1

   values
