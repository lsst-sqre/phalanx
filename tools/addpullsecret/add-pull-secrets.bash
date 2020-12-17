#!/usr/bin/env bash

# Requires Bash 4 because we use hashes; brew install bash if you're on
#  OS X (it's a GPL3 thing)

function usage() {
    echo 1>&2 "Usage: $0 lsp-deploy-directory"
    exit 1
}

bv=$(echo ${BASH_VERSION} | cut -d '.' -f 1)
if [ ${bv} -lt 4 ]; then
    echo 1>&2 "$0 requires at least bash version 4"
    exit 2
fi

# Customize as necessary
topdir=$1

if [ -z "${topdir}" ]; then
    usage
fi
if [ -n "$2" ]; then
    usage
fi

# This builds a list of services that have associated namespaces.
#  For instance, cert-manager and cert-issuer share a namespace; we only
#  inject a vault secret for pull once per namespace
svcs="argocd cert-manager exposurelog gafaelfawr influxdb kapacitor"
svcs="${svcs} landing-page mobu nginx-ingress nublado obstap portal"
svcs="${svcs} postgres tap wf"

# This is a list of environments.
envs="base bleed gold-leader idfdev int kueyen minikube nts nublado"
envs="${envs} red-five rogue-two stable summit tucson-teststand"

# These are the services that we're going to add the pull-secret string to:
#  Skip cachemachine and nublado2 for now.
add_pull="tap obstap exposurelog portal gafaelfawr influxdb kapacitor"
add_pull="${add_pull} landing-page mobu nublado postgres"

# This is what I have run it with so far.
#envs="nublado"

IFS='' read -r -d '' addreq <<'EOF'
- name: pull-secret
  version: 0.1.2
  repository: https://lsst-sqre.github.io/charts/
EOF

declare -A pull_secret
for e in ${envs}; do
    np="${topdir}/services/nublado/values-${e}.yaml"
    if ! [ -e ${np} ]; then
	echo 1>&2 "No nublado to query for secret path in env ${e}!"
	continue
    fi
    tops=$(grep "secret/k8s_operator" ${np} | head -1 | cut -d / -f 3 )
    if [ -z "${tops}" ] ;then
	echo 1>&2 "Could not determine vault secret path for ${e}."
	continue
    fi
    pull_secret[${e}]="secret/k8s_operator/${tops}/pull-secret"
done
for s in ${svcs}; do
    svcdir="${topdir}/services/${s}"
    for e in ${envs}; do
	psp="${pull_secret[${e}]}"
	if [ -z "${psp}" ]; then
	    echo 1>&2 "No vault secret path for ${e}."
	    continue
	fi
	IFS='' read -r -d '' addsec <<EOF

pull-secret:
  enabled: true
  path: ${psp}
EOF
	efile="${svcdir}/values-${e}.yaml"
	# if it doesn't exist, then it's OK to create it.
	if ! [ -e ${efile} ]; then
	    if [ -e ${svcdir}/values.yaml ]; then
		cp ${svcdir}/values.yaml ${efile}
	    fi
	fi
	grep -q "^pull-secret:" ${efile} 2>/dev/null
	rc=$?
	if [ ${rc} -eq 0 ] ; then
	    echo 1>&2 "${efile} already has pull-secret."
	else
	    echo -n "${addsec}" >> ${efile}
	fi
    done
    # Add pull-secret to requirements file.
    # nginx-ingress has its dependencies right in Chart.yaml
    rfile="${svcdir}/requirements.yaml"
    if [ "${s}" == "nginx-ingress" ]; then
	rfile="${svcdir}/Chart.yaml"
    fi
    grep -q "pull-secret" ${rfile} 2>/dev/null
    rc=$?
    if [ ${rc} -eq 0 ] ; then
	echo 1>&2 "${rfile} already has pull-secret."
    else
	echo -n "${addreq}" >> ${rfile}
    fi
done

for ap in ${add_pull}; do
    for e in ${envs}; do
	chartname=${ap}
	case ${ap} in
	    tap)
		chartname="cadc-tap"
		;;
	    obstap)
		chartname="cadc-tap-postgres"
		;;
	    portal)
		chartname="firefly"
		;;
	    *)
		;;
	esac
	svcdir="${topdir}/services/${ap}"
	efile="${svcdir}/values-${e}.yaml"
	if [ ! -e ${efile} ]; then # Don't add it if it doesn't exist.
	    continue
	fi
	# We also need to check for pull_secret being defined in the
	#  top-level app: this is the glue to actually enable it.
	grep -q '^  pull_secret:' ${efile}
	rc=$?
	if [ ${rc} -eq 0 ] ; then
	    echo 1>&2 "${efile} already has pull_secret."
	else
	    # Do we have the first line of the values file equalling the
	    #  key?  If not, make it so.
	    head -n 1 ${efile} | grep -q "^${chartname}:"
	    rc=$?
	    # Sorry about the newlines; running on macOS and real BSD sed
	    if [ ${rc} -ne 0 ]; then
		sed -i .init "0 a \\
${chartname}:
" ${efile}
	    fi
	    sed  -i .bak "1 a \\
  pull_secret: 'pull-secret'
" ${efile}
	fi
    done
done
exit 0
