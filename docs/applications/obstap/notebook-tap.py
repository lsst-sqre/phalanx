from diagrams import Cluster, Edge
from diagrams.gcp.compute import KubernetesEngine
from diagrams.gcp.database import SQL, Datastore, Memorystore
from diagrams.gcp.network import LoadBalancing
from diagrams.onprem.client import User
from sphinx_diagrams import SphinxDiagram

with SphinxDiagram(title="Notebook to TAP"):
    user = User("End User")

    with Cluster("Kubernetes"):
        ingress = LoadBalancing("NGINX Ingress")

        with Cluster("Nublado"):
            hub = KubernetesEngine("Hub")
            proxy = KubernetesEngine("Proxy")
            notebook = KubernetesEngine("Notebook")
            proxy >> hub
            hub >> notebook
            proxy >> notebook

        with Cluster("TAP"):
            tap = KubernetesEngine("TAP")
            schema = SQL("MySQL Schema DB")
            uws = SQL("PostgreSQL UWS")

        with Cluster("Gafaelfawr"):
            gafaelfawr = KubernetesEngine("Gafaelfawr")
            redis = Memorystore("Redis")
            cloudsql = SQL("Cloud SQL")

    postgres = Datastore("postgres")

    user >> ingress >> proxy >> hub
    user >> ingress >> proxy >> notebook >> ingress
    ingress >> tap
    ingress >> Edge(label="auth subrequest") >> gafaelfawr
    tap >> Edge(label="token user-info") >> ingress
    ingress >> Edge(label="token user-info") >> gafaelfawr
    tap >> schema
    tap >> uws
    tap >> postgres
    gafaelfawr >> redis
    gafaelfawr >> cloudsql
