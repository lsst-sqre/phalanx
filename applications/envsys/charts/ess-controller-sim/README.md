# ess-controller-sim

Chart for the ess-controller simulator

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | This specifies the scheduling constraints of the pod |
| image | object | `{"pullPolicy":"Always","repository":"lsstts/ess-controller-x86_64","revision":null}` | This section holds the configuration of the container image |
| image.pullPolicy | string | `"Always"` | The policy to apply when pulling an image for deployment |
| image.repository | string | `"lsstts/ess-controller-x86_64"` | The Docker registry name of the container image |
| image.revision | string | `nil` | The revision of the container image |
| namespace | string | `"envsys"` | This is the namespace in which the ess-controller simulator will be placed |
| nodeSelector | object | `{}` | This allows the specification of using specific nodes to run the pod |
| resources | object | `{}` | This allows the specification of resources (CPU, memory) requires to run the container |
| tolerations | list | `[]` | This specifies the tolerations of the pod for any system taints |
