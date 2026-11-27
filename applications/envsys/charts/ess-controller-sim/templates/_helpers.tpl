{{/* vim: set filetype=mustache: */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "ess-controller-sim.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create image name from information
*/}}
{{- define "helpers.makeImage" -}}
{{- if kindIs "float64" .rev }}
{{- $rev := int .rev -}}
{{- printf "%s:%s.%03d" .repo .tag $rev }}
{{- else }}
{{- printf "%s:latest" .repo }}
{{- end }}
{{- end }}
