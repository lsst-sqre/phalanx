.. px-app-notes:: tap-schema

#################################
tap-schema architecture and notes
#################################

The TAP schema may vary by environment, depending on the tables and data available in that environment.
This is controlled by the `build-all script in the lsst/sdm_schemas repository <https://github.com/lsst/sdm_schemas/blob/main/tap-schema/build-all>`__.

Each variation of the schema is represented by a different Docker image, which is a MySQL server with the appropriate data preloaded.
Whenever a new version of `lsst/sdm_schemas <https://github.com/lsst/sdm_schemas>`__ is tagged, GitHub Actions builds and pushes all of those Docker images.

Each Science Platform environment then selects the schema to deploy by configuring which Docker image to use in its ``values-<environment>.yaml`` file.
