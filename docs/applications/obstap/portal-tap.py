from diagrams import Cluster, Edge
from diagrams.gcp.compute import KubernetesEngine
from diagrams.gcp.database import SQL, Datastore, Memorystore
from diagrams.gcp.network import LoadBalancing
from diagrams.onprem.client import User
from sphinx_diagrams import SphinxDiagram

with SphinxDiagram(title="Portal to TAP"):
    user = User("End User")

    with Cluster("Kubernetes"):
        ingress = LoadBalancing("NGINX Ingress")

        with Cluster("Portal"):
            portal_1 = KubernetesEngine("Portal")
            portal_2 = KubernetesEngine("Portal")
            portal_redis = Memorystore("Redis")
            portal_1 >> portal_redis
            portal_2 >> portal_redis

        with Cluster("TAP"):
            tap = KubernetesEngine("TAP")
            schema = SQL("MySQL Schema DB")
            uws = SQL("PostgreSQL UWS")

        with Cluster("Gafaelfawr"):
            gafaelfawr = KubernetesEngine("Gafaelfawr")
            redis = Memorystore("Redis")
            cloudsql = SQL("Cloud SQL")

    postgres = Datastore("postgres")

    user >> ingress >> portal_1 >> Edge(label="to TAP") >> ingress
    ingress >> portal_2 >> ingress
    ingress >> tap
    ingress >> Edge(label="auth subrequest") >> gafaelfawr
    tap >> Edge(label="token user-info") >> ingress
    ingress >> Edge(label="token user-info") >> gafaelfawr
    tap >> schema
    tap >> uws
    tap >> postgres
    gafaelfawr >> redis
    gafaelfawr >> cloudsql
