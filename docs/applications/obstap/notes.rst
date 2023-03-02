.. px-app-notes:: obstap

##########################
OBSTAP architecture and notes
##########################

The ``obstap`` application consists of the TAP Java web application, a PostgreSQL database used to track user job submissions (the backing store for the UWS_ protocol), and (on development deployments) a mock version of postgres.

.. diagrams:: notebook-tap.py

.. diagrams:: portal-tap.py
