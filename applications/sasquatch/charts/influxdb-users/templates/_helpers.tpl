{{/* vim: set filetype=mustache: */}}
{{/* Expand the chart name. */}}
{{- define "influxdb-users.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/* Create a fully qualified app name. */}}
{{- define "influxdb-users.fullname" -}}
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

{{/* Create the chart label. */}}
{{- define "influxdb-users.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/* Common labels. */}}
{{- define "influxdb-users.labels" -}}
helm.sh/chart: {{ include "influxdb-users.chart" . }}
{{ include "influxdb-users.selectorLabels" . }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/* Selector labels. */}}
{{- define "influxdb-users.selectorLabels" -}}
app.kubernetes.io/name: {{ include "influxdb-users.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/* Use the same Enterprise data image as the bootstrap Job. */}}
{{- define "influxdb-users.image" -}}
{{- printf "%s:%s-data" .Values.image.repository (.Values.image.tag | default .Chart.AppVersion) -}}
{{- end }}
