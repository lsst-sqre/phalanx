.. px-app:: schedview-static-pages

###############################################################
schedview-static-pages — Server for static pages from schedview
###############################################################

The schedview static pages "application" is a simple nginx web server
deployed to serve static web pages with scheduler monitoring and survey
progress reports. This web server is used instead of the global USDF
web page so that the gafaelfawr ingres can be used to limit access.

.. jinja:: schedview-static-pages
   :file: applications/_summary.rst.jinja

Guides
======

.. toctree::
   :maxdepth: 1

   values