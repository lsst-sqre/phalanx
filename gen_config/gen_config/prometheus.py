prometheus_config = {
    "argocd": {
        "application_controller": "http://argocd-application-controller-metrics.argocd.svc:8082/metrics",
        "notifications_controller": "http://argocd-notifications-controller-metrics.argocd.svc:9001/metrics",
        "redis": "http://argocd-redis-metrics.argocd.svc:9121/metrics",
        "repo_server": "http://argocd-repo-server-metrics.argocd.svc:8084/metrics",
        "server": "http://argocd-server-metrics.argocd.svc:8083/metrics",
        },
    "nublado2": {
        "hub": "http://hub.nublado2:8081/metrics",
    },
    "ingress-nginx": {
        "controller": "http://ingress-nginx-controller-metrics.ingress-nginx:10254/metrics",
    },
}
        
