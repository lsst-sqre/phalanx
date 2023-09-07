.. px-app-troubleshooting:: argocd

######################
Troubleshooting argocd
######################

.. _argocd-fix-corrupt-git-index:

Fixing a corrupt git index
==========================

The Git index for the cloned repository that controls the Argo CD apps is corrupted if an Argo CD app shows the following error:

.. code-block:: shell

    rpc error: code = Internal desc = Failed to fetch default: `git fetch origin --tags --force --prune` failed exit status 128: fatal: .git/index: index file smaller than expected

The Git repository needs to be removed and re-created by following these steps:

#. Find the ``argocd-repo-server`` pod and grep the logs:

    .. code-block:: shell

        pod=$(kubectl get pods -n argocd -l app.kubernetes.io/name=argocd-repo-server | grep argocd | awk '{print $1}')
        kubectl logs -n argocd $pod | grep -B1 "index file smaller than expected" | grep -B1 "execID"

#. In that grep, find the ``dir`` field. For example:

    .. code-block:: shell

        {"dir":"/tmp/_argocd-repo/35fe76f8-488a-4871-baaa-5f81d81331b1","execID":"a98af","level":"info","msg":"git fetch origin --tags --force --prune","time":"2023-06-13T18:48:12Z"}
        {"execID":"a98af","level":"error","msg":"`git fetch origin --tags --force --prune` failed exit status 128: fatal: .git/index: index file smaller than expected","time":"2023-06-13T18:48:12Z"}

#. Exec into the repo server pod:

    .. code-block:: shell

        kubectl exec -it -n argocd $pod -- /bin/bash

#. Using the directory found from the logs, execute:

    .. code-block:: shell

        rm /path/from/log/.git/index

The system will refresh itself automatically, so all the needs to be done further is wait and see if the error clears.