####################################
Changing charts and phalanx together
####################################

Quite often when working on RSP services you will find that you need
simultaneous changes to both the `charts repository <https://github.com/lsst-sqre/charts>`__ and the `phalanx repository <https://github.com/lsst-sqre/phalanx>`__.

You may not want to roll out the charts changes prior to the phalanx changes, but at the same time, the phalanx changes require the charts changes.

If the charts changes are low-risk--perhaps they just add new objects or settings--then it's often OK to release a new charts version, and then point phalanx at the new version.  Then you can just update in ArgoCD and it's all very easy.

This section, however, is about the times when it's risky to do that.

The bad news is, you can't do this via ArgoCD.  The good news is, it's pretty easy to do anyway, but you do need ``kubectl`` access to whatever cluster you're working on.  Ideally this is a local ``minikube`` cluster, but if you're, say, using an Apple Silicon Mac, or you need access to real data, maybe you're doing it in ``data-dev`` or ``data-int``.  

#. Make your changes to both charts and phalanx.

#. Ensure that you're using ``kubectl`` with a kubeconfig file giving access to the cluster you want to use.

#. Generate a new chart with ``helm package <dirname>`` in the ``charts/charts`` directory.  This will generate a .tgz package of the application.

#. In the correct phalanx ``services`` directory, update ``Chart.yaml`` to the new (unreleased) Chart version.  Then update phalanx with ``helm dependency build .`` .  This will try to download the dependent charts and will fail, because the version hasn't been released.  Create a ``charts`` directory if it doesn't already exist, and copy the tarball you created into the previous step into it.

#. Finally, run ``helm install . <app-name> --values=<appropriate-values-file>``.

The running version will be out of sync in ArgoCD until you release the charts and phalanx changes, but it is testable in the cluster at this point.
