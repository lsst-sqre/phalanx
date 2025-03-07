# love-nginx

Helm chart for the LOVE Nginx server.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity rules for the NGINX pod |
| image.pullPolicy | string | `"IfNotPresent"` | The pull policy on the NGINX image |
| image.repository | string | `"nginx"` | The NGINX image to use |
| image.tag | string | `"1.27.4"` | The tag to use for the NGINX image |
| imagePullSecrets | list | `[]` | The list of pull secrets needed for the images. If this section is used, each object listed can have the following attributes defined: _name_ (The label identifying the pull-secret to use) |
| ingress.annotations | object | `{}` | Annotations for the NGINX ingress |
| ingress.className | string | `"nginx"` | Assign the Ingress class name |
| ingress.hostname | string | `"love.local"` | Hostname for the NGINX ingress |
| ingress.httpPath | string | `"/"` | Path name associated with the NGINX ingress |
| ingress.pathType | string | `""` | Set the Kubernetes path type for the NGINX ingress |
| initContainers.frontend.image.pullPolicy | string | `"IfNotPresent"` | The pull policy to use for the frontend image |
| initContainers.frontend.image.repository | string | `"lsstts/love-frontend"` | The frontend image to use |
| initContainers.frontend.image.revision | int | `nil` | The cycle revision to add to the image tag |
| initContainers.manager.command | list | `["/bin/sh","-c","mkdir -p /usr/src/love-manager/media/thumbnails; mkdir -p /usr/src/love-manager/media/configs; cp -Rv /usr/src/love/manager/static /usr/src/love-manager; cp -uv /usr/src/love/manager/ui_framework/fixtures/thumbnails/* /usr/src/love-manager/media/thumbnails; cp -uv /usr/src/love/manager/api/fixtures/configs/* /usr/src/love-manager/media/configs"]` | The command to execute for the love-manager static content |
| initContainers.manager.image.pullPolicy | string | `"IfNotPresent"` | The pull policy to use for the love-manager static content image |
| initContainers.manager.image.repository | string | `"lsstts/love-manager"` | The static love-manager content image to use |
| initContainers.manager.image.revision | int | `nil` | The cycle revision to add to the image tag |
| loveConfig | string | `"{\n  \"alarms\": {\n    \"minSeveritySound\": \"serious\",\n    \"minSeverityNotification\": \"warning\"\n  },\n  \"camFeeds\": {\n    \"generic\": \"/gencam\",\n    \"allSky\": \"/gencam\"\n  }\n}\n"` | Configuration specificiation for the LOVE service |
| namespace | string | `"love"` | The overall namespace for the application |
| nginxConfig | string | `"server {\n  listen 80;\n  server_name localhost;\n  location / {\n    root   /usr/src/love-frontend;\n    try_files $uri$args $uri$args/ $uri/ /index.html;\n  }\n  location /manager {\n      proxy_pass http://love-manager-service:8000;\n      proxy_http_version 1.1;\n      proxy_set_header Upgrade $http_upgrade;\n      proxy_set_header Connection \"upgrade\";\n      proxy_set_header Host $host;\n      proxy_redirect off;\n  }\n  location /manager/static {\n      alias /usr/src/love-manager/static;\n  }\n  location /manager/media {\n      alias /usr/src/love-manager/media;\n  }\n}\n"` | Configuration specification for the NGINX service |
| nodeSelector | object | `{}` | Node selection rules for the NGINX pod |
| ports.container | int | `80` | Container port for the NGINX service |
| ports.node | int | `30000` | Node port for the NGINX service |
| resources | object | `{}` | Resource specifications for the NGINX pod |
| serviceType | string | `"ClusterIP"` | Service type specification |
| staticStore.accessMode | string | `"ReadWriteMany"` | The access mode for the NGINX static store |
| staticStore.claimSize | string | `"2Gi"` | The size of the NGINX static store request |
| staticStore.name | string | `"love-nginx-static"` | Label for the NGINX static store |
| staticStore.storageClass | string | `"local-store"` | The storage class to request the disk allocation from |
| tolerations | list | `[]` | Toleration specifications for the NGINX pod |
