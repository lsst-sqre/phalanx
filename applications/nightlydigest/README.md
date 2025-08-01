# nightlydigest

Nightlydigest logging and reporting service

## Source Code

* <https://github.com/lsst-ts/ts_logging_frontend>
* <https://github.com/lsst-ts/ts_logging_and_reporting>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| global.controlSystem.appNamespace | string | Set by ArgoCD | Application namespace for the control system deployment |
| global.controlSystem.imageTag | string | Set by ArgoCD | Image tag for the control system deployment |
| global.controlSystem.kafkaBrokerAddress | string | Set by ArgoCD | Kafka broker address for the control system deployment |
| global.controlSystem.kafkaTopicReplicationFactor | string | Set by ArgoCD | Kafka topic replication factor for control system topics |
| global.controlSystem.s3EndpointUrl | string | Set by ArgoCD | S3 endpoint (LFA) for the control system deployment |
| global.controlSystem.schemaRegistryUrl | string | Set by ArgoCD | Schema registry URL for the control system deployment |
| global.controlSystem.siteTag | string | Set by ArgoCD | Site tag for the control system deployment |
| global.controlSystem.topicName | string | Set by ArgoCD | Topic name tag for the control system deployment |
| global.host | string | Set by Argo CD | Host name for ingress |
| global.vaultSecretsPath | string | Set by Argo CD | Base path for Vault secrets |
| nightlydigest-backend.affinity | object | `{}` | Affinity rules applied to the pod. |
| nightlydigest-backend.annotations | object | `{}` | This allows for the specification of pod annotations. |
| nightlydigest-backend.env | object | `{}` | This section holds a set of key, value pairs for environmental variables. |
| nightlydigest-backend.envSecrets | object | `{}` | This section holds a set of key, value pairs for secrets. |
| nightlydigest-backend.image.pullPolicy | string | `"IfNotPresent"` | The pull policy on the Nightlydigest backend image. |
| nightlydigest-backend.image.repository | string | `"lsstts/nightlydigest-backend"` | The Nightlydigest backend image to use. |
| nightlydigest-backend.image.tag | int | `nil` | The cycle revision to add to the image tag. |
| nightlydigest-backend.namespace | string | `"nightlydigest"` | The overall namespace for the application. |
| nightlydigest-backend.nodeSelector | object | `{}` | Node selection rules applied to the pod. |
| nightlydigest-backend.resources | object | `{}` | Resource specifications applied to the pod. |
| nightlydigest-backend.tolerations | list | `[]` | Toleration specifications applied to the pod. |
| nightlydigest-nginx.affinity | object | `{}` | Affinity rules for the NGINX pod |
| nightlydigest-nginx.image.pullPolicy | string | `"IfNotPresent"` | The pull policy on the NGINX image |
| nightlydigest-nginx.image.repository | string | `"nginx"` | The NGINX image to use |
| nightlydigest-nginx.image.tag | string | `"1.29.0"` | The tag to use for the NGINX image |
| nightlydigest-nginx.imagePullSecrets | list | `[]` | The list of pull secrets needed for the images. If this section is used, each object listed can have the following attributes defined: _name_ (The label identifying the pull-secret to use) |
| nightlydigest-nginx.ingress.annotations | object | `{}` | Annotations for the NGINX ingress |
| nightlydigest-nginx.ingress.className | string | `"nginx"` | Assign the Ingress class name |
| nightlydigest-nginx.ingress.hostname | string | `"nightlydigest.local"` | Hostname for the NGINX ingress |
| nightlydigest-nginx.ingress.httpPath | string | `"/"` | Path name associated with the NGINX ingress |
| nightlydigest-nginx.ingress.pathType | string | `""` | Set the Kubernetes path type for the NGINX ingress |
| nightlydigest-nginx.initContainers.frontend.image.pullPolicy | string | `"IfNotPresent"` | The pull policy to use for the frontend image |
| nightlydigest-nginx.initContainers.frontend.image.repository | string | `"lsstts/nightlydigest-frontend"` | The frontend image to use |
| nightlydigest-nginx.initContainers.frontend.image.tag | int | `nil` | The cycle revision to add to the image tag |
| nightlydigest-nginx.namespace | string | `"nightlydigest"` | The overall namespace for the application |
| nightlydigest-nginx.nginxConfig | string | `"server {\n  listen 80;\n  server_name localhost;\n  location / {\n    root   /usr/src/frontend;\n    try_files $uri$args $uri$args/ $uri/ /index.html;\n  }\n}\n"` | Configuration specification for the NGINX service |
| nightlydigest-nginx.nodeSelector | object | `{}` | Node selection rules for the NGINX pod |
| nightlydigest-nginx.ports.container | int | `80` | Container port for the NGINX service |
| nightlydigest-nginx.ports.node | int | `30000` | Node port for the NGINX service |
| nightlydigest-nginx.resources | object | `{}` | Resource specifications for the NGINX pod |
| nightlydigest-nginx.serviceType | string | `"ClusterIP"` | Service type specification |
| nightlydigest-nginx.staticStore.accessMode | string | `"ReadWriteMany"` | The access mode for the NGINX static store |
| nightlydigest-nginx.staticStore.claimSize | string | `"2Gi"` | The size of the NGINX static store request |
| nightlydigest-nginx.staticStore.name | string | `"nightlydigest-nginx-static"` | Label for the NGINX static store |
| nightlydigest-nginx.staticStore.storageClass | string | `"local-store"` | The storage class to request the disk allocation from |
| nightlydigest-nginx.tolerations | list | `[]` | Toleration specifications for the NGINX pod |
