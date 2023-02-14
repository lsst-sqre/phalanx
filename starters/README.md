# Helm starters for Phalanx

Each subdirectory of this directory is a Helm starter for a class of Phalanx service.
Use the starters with the `-p` option to `helm create`.
For example, from the `applications` directory:

```sh
helm create new-service -p $(pwd)/../starters/rsp-web-service
```

The path to the starter directory must be absolute, not relative, or Helm will try to use it has a path relative to `$HOME/.local/share/helm`.
