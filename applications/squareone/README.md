# squareone

Squareone is the homepage UI for the Rubin Science Platform.

**Homepage:** <https://squareone.lsst.io/>

## Source Code

* <https://github.com/lsst-sqre/squareone>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` |  |
| autoscaling.enabled | bool | `false` |  |
| autoscaling.maxReplicas | int | `100` |  |
| autoscaling.minReplicas | int | `1` |  |
| autoscaling.targetCPUUtilizationPercentage | int | `80` |  |
| config.apiAspectPageMdx | string | `"# Rubin Science Platform APIs\n\n<Lede>Integrate Rubin data into your analysis tools with APIs.</Lede>\n\nTo access most APIs you need an [*access token*](/auth/tokens).\nSee our guide [Creating user tokens](https://rsp.lsst.io/guides/auth/creating-user-tokens.html) to learn more.\n\n## Table Access Protocol\n\nYou can access catalog data using the Table Access Protocol (TAP)\nservice with popular tools such as\n[TOPCAT](http://www.star.bris.ac.uk/~mbt/topcat) (GUI) and\n(pyvo)[https://pyvo.readthedocs.io/en/latest/index.html]\n(Python package). The TAP endpoint is:\n\n```\nhttps://data.lsst.cloud/api/tap\n```\n\nSee our tutorial [Authenticating from TOPCat outside the Science Platform](https://rsp.lsst.io/guides/auth/using-topcat-outside-rsp.html)\nto learn more about accessing TAP datasets from your own computer.\n"` | MDX content for the `/api-aspect` page |
| config.coManageRegistryUrl | string | `nil` | URL to the COmanage registry, if the environment uses COmanage for identity. @default null disables the COmanage integration |
| config.docsPageMdx | string | `"# Rubin Science Platform documentation\n\n<Lede>Find documentation for Rubin Observatory data, science platform\nservices, and software.</Lede>\n\n<Section>\n\n  ## Data documentation\n\n  <CardGroup>\n    <a href=\"https://dp0-2.lsst.io/\">\n      <Card>\n        ### Data Preview 0.2 (DP0.2)\n\n        DP0.2 is the second phase of the Data Preview 0 program using\n        precursor data (simulated images from the DESC DC2 data\n        challenge). For the first time, all the derived data products\n        have been generated “in-house” on an early version of the Rubin\n        processing infrastructure using version 23.0 of the LSST Science\n        Pipelines. As a result, the data model is significantly\n        different from the DP0.1 dataset.\n      </Card>\n    </a>\n\n    <a href=\"https://dm.lsst.org/sdm_schemas/browser/dp02.html\">\n      <Card>\n        ### DP0.2 Catalog Schema\n\n        Schema reference for the DP0.2 catalog dataset available through\n        the Table Access Protocol (TAP) service.\n      </Card>\n    </a>\n  </CardGroup>\n</Section>\n\n<Section>\n\n  ## Platform and software documentation\n\n  <CardGroup>\n    <a href=\"https://rsp.lsst.io\">\n      <Card>\n        ### Rubin Science Platform\n\n        The Notebook aspect is a powerful data analysis environment with\n        Jupyter Notebooks and terminals in the browser.\n        Documentation for the Rubin Science Platform, including account set up,\n        portal, notebooks, and API aspects.\n      </Card>\n    </a>\n\n    <a href=\"/portal/app/onlinehelp/\">\n      <Card>\n        ### Portal\n\n        The Portal enables you to explore LSST image and table data in\n        your browser.\n      </Card>\n    </a>\n\n    <a href=\"https://pipelines.lsst.io\">\n      <Card>\n        ### LSST Science Pipelines\n\n        The Science Pipelines include the Butler for accessing LSST data\n        and a pipeline framework for processing data. The LSST Science\n        Pipelines Python package is preinstalled in the Notebook aspect.\n      </Card>\n    </a>\n\n  </CardGroup>\n</Section>\n\n<Section>\n\n  ## Have more questions?\n\n  <Link href=\"/support\">Learn how to get support or report issues.</Link>\n\n  Want to dive deeper into the Rubin Observatory and Legacy Survey of\n  Space and Time? [Search in our technical documentation\n  portal.](https://www.lsst.io)\n\n</Section>\n"` | MDX content for the `/docs` page |
| config.emailVerifiedPageMdx | string | `"# Your email is verified\n\n<Lede>We are reviewing your application. You’ll receive an email as soon as\nyour account is approved.</Lede>\n"` | MDX content for the `/enrollment/thanks-for-verifying` page |
| config.pendingApprovalPageMdx | string | `"# Your account is pending approval\n\n<Lede>Requests are typically processed within five business days.</Lede>\n\nOnce your account is approved, you’ll receive an email at the address\nyou registered with.\n\n<Link href=\"../support\"><a>Contact us</a></Link> if you have further questions.\n"` | MDX content for the `/enrollment/pending-approval` page |
| config.pendingVerificationPageMdx | string | `"# Please confirm your email\n\n<Lede>Your email is still pending verification.</Lede>\n\nTo complete your enrollment please check the email you registered with\nfor a link to verify your email address. Please click on the link to\nverify your email address.\n\nIf you have not received the confirmation email please check your SPAM folder.\n\nIf you still cannot find the confirmation email please\n<Link href=\"../support\"><a>contact us</a></Link> to have the confirmation\nemail resent.\n"` | MDX content for the `/enrollment/pending-confirmation` |
| config.semaphoreUrl | string | `nil` | URL to the Semaphore (user notifications) API service. @default null disables the Semaphore integration |
| config.siteDescription | string | `"Access Rubin Observatory Legacy Survey of Space and Time data.\n"` | Site description, used in meta tags |
| config.siteName | string | `"Rubin Science Platform"` | Name of the site, used in the title and meta tags. |
| config.supportPageMdx | string | `"# Get help with the Rubin Science Platform\n\n<Lede>Besides the <Link href=\"/docs\">documentation</Link>, you can get help\nfrom Rubin Observatory staff. Here are the ways to ask for help.</Lede>\n\n<Section>\n  ## Data Preview 0 science questions\n\n  For questions about the Data Preview dataset (DESC DC2) and analyzing\n  that data (such as with the LSST Science Pipelines), create a new\n  topic in the [Data Preview 0 Support category](https://community.lsst.org/c/support/dp0/49)\n  of the Community forum.\n\n  <CtaLink href=\"http://community.lsst.org/new-topic?category=support/dp0\">Create a science support topic in the forum</CtaLink>\n</Section>\n\n<Section>\n  ## Rubin Science Platform technical support and feature requests\n\n  For technical issues or feature requests related to the Rubin Science\n  Platform itself (the Portal, Notebooks, and API services such as TAP)\n  create a GitHub issue in the\n  [rubin-dp0/Support](https://github.com/rubin-dp0/Support) repository.\n\n  <CtaLink href=\"https://github.com/rubin-dp0/Support/issues/new/choose\">Create a GitHub issue</CtaLink>\n</Section>\n"` | MDX content for the `/support` page |
| config.timesSquareUrl | string | `nil` | URL to the Times Square (parameterized notebooks) API service. @default null disables the Times Square integration |
| config.verifyEmailPageMdx | string | `"# Thanks for registering\n\n<Lede>You'll receive an email from us shortly. Click on the link in the\nmessage to verify your address and continue your account set up.</Lede>\n"` | MDX content for the `/enrollment/thanks-for-signing-up` page |
| fullnameOverride | string | `""` | Overrides the full name for resources (includes the release name) |
| global.baseUrl | string | Set by Argo CD Application | Base URL for the environment |
| global.host | string | Set by Argo CD Application | Host name for ingress |
| global.vaultSecretsPathPrefix | string | Set by Argo CD Application | Base path for Vault secrets |
| image.pullPolicy | string | `"IfNotPresent"` | Image pull policy (tip: use Always for development) |
| image.repository | string | `"ghcr.io/lsst-sqre/squareone"` | Squareone Docker image repository |
| image.tag | string | Chart's appVersion | Overrides the image tag. |
| ingress.annotations | object | `{}` | Additional annotations to add to the ingress |
| ingress.enabled | bool | `true` | Enable ingress |
| ingress.tls | bool | `true` | Enable Let's Encrypt TLS management in this chart. This should be false if TLS is managed elsewhere, such as in an ingress-nginx app. |
| nameOverride | string | `""` | Overrides the base name for resources |
| nodeSelector | object | `{}` |  |
| podAnnotations | object | `{}` | Annotations for squareone pods |
| replicaCount | int | `1` | Number of squareone pods to run in the deployment. |
| resources | object | `{}` |  |
| tolerations | list | `[]` |  |
