.. px-app-bootstrap:: argo-cd

#####################
Bootstrapping Argo CD
#####################

Initial installation of the Rubin Science Platform is done using Argo CD and a static password for the ``admin`` account.
You can then log on to the ``admin`` account using that password to manage the resulting environment.
No special bootstrapping is required.

That said, using the ``admin`` account for longer than necessary is not recommended.
Instead, you should configure single sign-on for Argo CD as soon as possible and prefer that for day-to-day operations to minimize the chances of leaking the ``admin`` password.

To do that, follow the instructions in :doc:`authentication`.

You may want to do this during your initial bootstrapping process, or very shortly afterwards.
The execution of the installer script itself will use the ``admin`` account and password regardless, but if Argo CD SSO is set up in advance, you can then immediately switch to using it for management of the environment.
