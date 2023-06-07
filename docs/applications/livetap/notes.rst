.. px-app-notes:: livetap

##############################
LiveTAP architecture and notes
##############################

The ``livetap`` application consists of the TAP Java web application, a PostgreSQL database used to track user job submissions (the backing store for the UWS_ protocol), and (on development deployments) a mock version of postgres.  There is a table that is updated by the butler to keep a live version of the ObsCore table.

.. diagrams:: notebook-tap.py

.. diagrams:: portal-tap.py
