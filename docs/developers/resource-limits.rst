############################
Resource requests and limits
############################

Every container in a Phalanx application should have Kubernetes CPU and memory resource requests and limits set.
This helps Kubernetes correctly reserve resources for pods and stop resource consumption bugs from causing problems for other services.
Many existing applications are missing resource requests and limits, but we are slowly trying to add them.

The ``web-service`` template sets up configurable resource limits with the :file:`values.yaml` ``resources`` setting, and appropriate templating in the :file:`templates/deployment.yaml`.
If your application is more complex, you will probably want separate ``resources`` settings for each component of your application that creates pods.

The best way to determine what resource requests and limits are correct for your application is to run the application under normal load and then see what CPU and memory the pods required.
If your application is running in an environment hosted on Google Kubernetes Engine and you have access to the Google Cloud console, find your pod under :menuselection:`Kubernetes Engine --> Workloads` and look at the CPU and memory graphs.
You can change the time range to see your application's average and peak resource consumption.
