# nightlydigest-nginx

Helm chart for the Nightlydigest Nginx server.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the NGINX pod |
| image.pullPolicy | string | `"IfNotPresent"` | The pull policy on the NGINX image |
| image.repository | string | `"nginx"` | The NGINX image to use |
| image.tag | string | `"1.28.0"` | The tag to use for the NGINX image |
| imagePullSecrets | list | `[]` | The list of pull secrets needed for the images. If this section is used, each object listed can have the following attributes defined: _name_ (The label identifying the pull-secret to use) |
| ingress.annotations | object | `{}` | Annotations for the NGINX ingress |
| ingress.className | string | `"nginx"` | Assign the Ingress class name |
| ingress.hostname | string | `"nightlydigest.local"` | Hostname for the NGINX ingress |
| ingress.httpPath | string | `"/"` | Path name associated with the NGINX ingress |
| ingress.pathType | string | `""` | Set the Kubernetes path type for the NGINX ingress |
| initContainers.frontend.image.pullPolicy | string | `"IfNotPresent"` | The pull policy to use for the frontend image |
| initContainers.frontend.image.repository | string | `"lsstts/nightlydigest-frontend"` | The frontend image to use |
| initContainers.frontend.image.tag | int | `nil` | The cycle revision to add to the image tag |
| namespace | string | `"nightlydigest"` | The overall namespace for the application |
| nginxConfig | string | `"server {\n  listen 80;\n  server_name localhost;\n  location / {\n    root   /usr/src/frontend;\n    try_files $uri$args $uri$args/ $uri/ /index.html;\n  }\n}\n"` | Configuration specification for the NGINX service |
| nodeSelector | object | `{}` | Node selection rules for the NGINX pod |
| ports.container | int | `80` | Container port for the NGINX service |
| ports.node | int | `30000` | Node port for the NGINX service |
| resources | object | `{}` | Resource specifications for the NGINX pod |
| serviceType | string | `"ClusterIP"` | Service type specification |
| staticStore.accessMode | string | `"ReadWriteMany"` | The access mode for the NGINX static store |
| staticStore.claimSize | string | `"2Gi"` | The size of the NGINX static store request |
| staticStore.name | string | `"nightlydigest-nginx-static"` | Label for the NGINX static store |
| staticStore.storageClass | string | `"local-store"` | The storage class to request the disk allocation from |
| tolerations | list | `[]` | Toleration specifications for the NGINX pod |
