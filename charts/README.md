# Shared Phalanx charts

This directory contains Helm charts that are shared between multiple Phalanx applications (in the `applications` directory), but which do not need to have an existence independent of Phalanx.

The charts in this directory are an optimization to avoid reptition, not stand-alone Helm charts.
They are only supported in conjunction with the applications that reference them.
All charts in this directory should have the version `1.0.0`, similar to all Phalanx application charts.

To use a chart in this directory, use a dependency stanza similar to the following in the Phalanx application:

```yaml
dependencies:
  - name: cadc-tap
    version: 1.0.0
    repository: "file://../../charts/cadc-tap"
```

If a Helm chart should be usable independently of Phalanx and warrants a separate existence with its own version number, that chart should instead go into the [charts](https://github.com/lsst-sqre/charts) repository.
