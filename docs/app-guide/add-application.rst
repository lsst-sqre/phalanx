###################
Add new application
###################

Add a directory to `/services <https://github.com/lsst-sqre/phalanx/tree/master/services>`__ named for the application (which should normally be the same as the name of its chart to avoid excessively long names).
Then add a ``Chart.yaml`` file and ``values-<enviornment>.yaml`` files for each environment in which that application will be deployed.

You can then cargo-cult the changes to the `science-platform application <https://github.com/lsst-sqre/phalanx/tree/master/science-platform>`__ to add a new application and the various configuration on/off switches per environment.
