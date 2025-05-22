{{/*
Expand the name of the chart.
*/}}
{{- define "nightlydigest-nginx.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "nightlydigest-nginx.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "nightlydigest-nginx.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create image name from information
*/}}
{{- define "helpers.makeImage" -}}
{{- if kindIs "float64" .rev }}
{{- $rev := int .rev -}}
{{- printf "%s:%s.%03d" .repo .tag $rev }}
{{- else }}
{{- printf "%s:%s" .repo .tag }}
{{- end }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "nightlydigest-nginx.labels" -}}
helm.sh/chart: {{ include "nightlydigest-nginx.chart" . }}
{{ include "nightlydigest-nginx.selectorLabels" . }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "nightlydigest-nginx.selectorLabels" -}}
app.kubernetes.io/name: {{ include "nightlydigest-nginx.name" . }}
app.kubernetes.io/instance: {{ include "nightlydigest-nginx.name" . }}
{{- end }}
