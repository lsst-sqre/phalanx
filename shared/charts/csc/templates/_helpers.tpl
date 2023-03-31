{{/* vim: set filetype=mustache: */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "chart.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "chart.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- include "chart.name" -}}
{{- end -}}
{{- end -}}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "chart.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create the CSC name by removing sim tag.
*/}}
{{- define "csc.name" -}}
{{- if contains "sim" .Chart.Name -}}
{{- .Chart.Name | splitList "-" | first -}}
{{- else -}}
{{- .Chart.Name -}}
{{- end -}}
{{- end -}}

{{/*
Create the CSC class name by removing sim tag and index.
*/}}
{{- define "csc.class" -}}
{{- $protectedApps := list "mtm2" "mtm1m3" -}}
{{- $name := .Chart.Name -}}
{{- if contains "sim" .Chart.Name -}}
{{- $name = $name | splitList "-" | first -}}
{{- end -}}
{{- $checkForIndex := list -}}
{{- if not (has $name $protectedApps) -}}
{{- $checkForIndex = regexFindAll "[0-9]+$" $name -1 -}}
{{- end -}}
{{- if $checkForIndex -}}
{{- $index := first $checkForIndex -}}
{{- $name = regexReplaceAll $index $name "" -}}
{{- end -}}
{{- $name -}}
{{- end -}}

{{/*
Common labels
*/}}
{{- define "csc.labels" -}}
helm.sh/chart: {{ .Chart.Name }}
{{ include "csc.selectorLabels" . }}
{{- end -}}

{{/*
Selector labels
*/}}
{{- define "csc.selectorLabels" -}}
csc: {{ include "chart.name" . }}
csc-name: {{ include "csc.name" . }}
csc-class: {{ include "csc.class" . }}
csc-is-primary: {{ .Values.isPrimary }}
{{- end -}}
