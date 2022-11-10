Shared charts
=============

This directory holds Helm charts that are shared by multiple services deployed as by Phalanx, but which themselves are not services or used external to Phalanx.
Charts that may be used external to Phalanx should instead go into the [charts repository](https://github.com/lsst-sqre/charts), where they can be published as proper Helm charts.

To use a chart in this directory:

#. Create a `charts` subdirectory of the service, if one does not already exist.
#. From that directory, create a relative symlink (starting with `../../..`) to the chart in this directory that you want to use.
#. Add that chart to `Chart.yaml` for your service under `dependencies`.
   The version should be `1.0.0` since all charts in this directory should always use version `1.0.0`.
