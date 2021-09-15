from diagrams import Cluster, Diagram, Edge
from diagrams.gcp.compute import KubernetesEngine
from diagrams.gcp.database import Datastore, Memorystore, SQL
from diagrams.gcp.network import LoadBalancing
from diagrams.onprem.client import User

with Diagram(
        "Portal to TAP",
        show=False,
        filename="portal-tap",
        outformat="png",
):
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

    qserv = Datastore("qserv")

    user >> ingress >> portal_1 >> Edge(label="to TAP") >> ingress
    ingress >> portal_2 >> ingress
    ingress >> tap
    ingress >> Edge(label="auth subrequest") >> gafaelfawr
    tap >> Edge(label="token user-info") >> ingress
    ingress >> Edge(label="token user-info") >> gafaelfawr
    tap >> schema
    tap >> uws
    tap >> qserv
    gafaelfawr >> redis
    gafaelfawr >> cloudsql
