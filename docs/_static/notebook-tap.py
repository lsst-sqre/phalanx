import os

from diagrams import Cluster, Diagram, Edge
from diagrams.gcp.compute import KubernetesEngine
from diagrams.gcp.database import SQL, Datastore, Memorystore
from diagrams.gcp.network import LoadBalancing
from diagrams.onprem.client import User

os.chdir(os.path.dirname(__file__))

with Diagram(
    "Notebook to TAP",
    show=False,
    filename="notebook-tap",
    outformat="png",
):
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

    qserv = Datastore("qserv")

    user >> ingress >> proxy >> hub
    user >> ingress >> proxy >> notebook >> ingress
    ingress >> tap
    ingress >> Edge(label="auth subrequest") >> gafaelfawr
    tap >> Edge(label="token user-info") >> ingress
    ingress >> Edge(label="token user-info") >> gafaelfawr
    tap >> schema
    tap >> uws
    tap >> qserv
    gafaelfawr >> redis
    gafaelfawr >> cloudsql
