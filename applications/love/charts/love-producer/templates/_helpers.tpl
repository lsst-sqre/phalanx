{{/*
Expand the name of the chart.
*/}}
{{- define "love-producer.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "love-producer.fullname" -}}
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
Create app name from release and producer name.
*/}}
{{- define "love-producer.appName" -}}
{{ printf "%s-producer-%s" .Release.Name .Producer | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "love-producer.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "love-producer.labels" -}}
helm.sh/chart: {{ include "love-producer.chart" . }}
{{ include "love-producer.selectorLabels" . }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "love-producer.selectorLabels" -}}
app.kubernetes.io/name: {{ include "love-producer.name" . }}
{{- end }}
