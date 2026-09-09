###########
Autoscaling
###########

Kubernetes workloads can be autoscaled using either `horizontal pod autoscaling`_ or `vertical pod autoscaling`_.
Horizontal autoscaling means adding and removing pods from a workload, and vertical autoscaling means increasing or decreasing the resources allocated to pods in a workload.
We don't currently use vertical autoscaling for any Phalanx apps, so we don't have any best practices.
We will add them here when we have them.

Horizontal pod autoscaling
==========================

Implement horizontal pod autoscaling by creating a `HorizontalPodAutoscaler`_ (HPA) resource.
You can configure this resource to tell Kubernetes to create and destroy pods in a workload to keep the value for a given metric (or set of metrics) close to a specified value.
You can scale based on CPU usage or memory usage.
For each of those resource types, you can scale based on percentage of utilization of the **request**, or an absolute value, like ``500m`` for CPU or ``2Gi`` for memory.

Autoscaling Python apps
-----------------------

.. note::

   Unless you are using `multiprocessing`_ or `Uvicorn`_/`Gunicorn`_ with multiple worker processes, a typical Python container will never use more than 1 CPU.

When you specify a utilization percentage, you are specifying the percentage of the **request** of a resource used, not the limit.
If you're trying to autoscale a Python application based on CPU usage, you may want to scale based on an absolute value rather than a utilization percentage.

Consider a workload with resources specified like this, where you want to keep the average CPU usage among all of the replicas around ``750m``.
In other words, if average CPU usage goes significantly higher than ``750m``, you want to add more pods. If it goes significantly lower than ``750m``, you want to remove pods.

.. code-block:: yaml
   :caption: deployment.yaml

   apiVersion: apps/v1
   kind: Deployment
   spec:
   ...
     template:
       ...
       spec:
         ...
         containers:
         - resources:
             limits:
               cpu: 1
               memory: 300Mi
             requests:
               cpu: 50m
               memory: 145Mi

You might initally come up with an HPA that looks like this:

.. admonition:: bad-hpa.yaml
   :class: danger


   .. code-block:: yaml
      :emphasize-lines: 9

      apiVersion: autoscaling/v2
      kind: HorizontalPodAutoscaler
      spec:
        ...
        metrics:
        - resource:
            name: cpu
            target:
              averageUtilization: 75
              type: Utilization
          type: Resource

But this will trigger a scale-up when the average CPU usage among all pods is 75% of ``50m``, or ``37m``, which would be much too fast.
You could calculate what percentage (over 100) of the request to specify to equal 75% of a single CPU, but it's easier to directly specify a value of ``750m`` and not depend on the request value at all:


.. admonition:: good-hpa.yaml
   :class: tip

   .. code-block:: yaml
      :emphasize-lines: 9

      apiVersion: autoscaling/v2
      kind: HorizontalPodAutoscaler
      spec:
        ...
        metrics:
        - resource:
            name: cpu
            target:
              averageValue: 750m
              type: AverageValue
          type: Resource
