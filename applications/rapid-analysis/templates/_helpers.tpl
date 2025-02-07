{{/*
Expand the name of the chart.
*/}}
{{- define "rapid-analysis.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "rapid-analysis.fullname" -}}
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
{{- define "rapid-analysis.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "rapid-analysis.labels" -}}
helm.sh/chart: {{ include "rapid-analysis.chart" . }}
{{ include "rapid-analysis.selectorLabels" . }}
{{- end }}

{{/*
Script name
*/}}
{{- define "rapid-analysis.scriptName" -}}
{{- regexSplit "/" .Values.script.name -1 | last | trimSuffix ".py" | kebabcase }}
{{- end }}

{{/*
Deployment name
*/}}
{{- define "rapid-analysis.deploymentName" -}}
{{- $values := regexSplit "/" .Values.script.name -1 }}
{{- $name := $values | last | trimSuffix ".py" | kebabcase }}
{{- if eq 2 (len $values) }}
{{- $cameraName := $values | first | lower }}
{{- $camera := "" }}
{{- if eq $cameraName "auxtel" }}
{{- $camera = "at"}}
{{- else if eq $cameraName "comcam" }}
{{- $camera = "cc"}}
{{- else }}
{{- $camera = $cameraName}}
{{- end }}
{{- printf "s-%s-%s" $camera $name }}
{{- else if eq 3 (len $values) }}
{{- $cameraName := $values | rest | first | lower }}
{{- $camera := "" }}
{{- if eq $cameraName "auxtel" }}
{{- $camera = "at"}}
{{- else if eq $cameraName "comcam" }}
{{- $camera = "cc"}}
{{- else }}
{{- $camera = $cameraName}}
{{- end }}
{{- printf "s-%s-%s" $camera $name }}
{{- end }}
{{- end }}


{{/*
Selector labels
*/}}
{{- define "rapid-analysis.selectorLabels" -}}
app.kubernetes.io/name: {{ include "rapid-analysis.deploymentName" . }}
app.kubernetes.io/instance: {{ include "rapid-analysis.name" . }}
{{- $values := regexSplit "/" .Values.script.name -1 }}
{{- if eq 1 (len $values) }}
all: misc
{{- else if eq 2 (len $values) }}
{{- $all_label := lower (index $values 0) }}
{{- $script := index $values 1 }}
{{- if contains "Isr" $script }}
isr: {{ $all_label }}
{{- end }}
all: {{ $all_label }}
{{- if has $all_label (list "auxtel" "comcam" "bot" "ts8") }}
camera: {{ $all_label }}
{{- else }}
{{- if contains "StarTracker" $script }}
camera: startracker
{{- end }}
{{- end }}
{{- else if eq 3 (len $values) }}
{{- $all_label := lower (index $values 1) }}
{{- $script := index $values 2 }}
{{- if contains "Isr" $script }}
isr: {{ $all_label }}
{{- end }}
all: {{ $all_label }}
{{- if has $all_label (list "auxtel" "comcam" "bot" "ts8") }}
camera: {{ $all_label }}
{{- else }}
{{- if contains "StarTracker" $script }}
camera: startracker
{{- end }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create a default fully qualified app name for redis.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "rapid-analysis.redis.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- printf "%s-redis" .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s-redis" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Common labels - redis
*/}}
{{- define "rapid-analysis.redis.labels" -}}
helm.sh/chart: {{ include "rapid-analysis.chart" . }}
{{ include "rapid-analysis.redis.selectorLabels" . }}
{{- end }}

{{/*
Selector labels - redis
*/}}
{{- define "rapid-analysis.redis.selectorLabels" -}}
app.kubernetes.io/name: {{ include "rapid-analysis.name" . }}
app.kubernetes.io/instance: {{ include "rapid-analysis.redis.fullname" . }}
{{- end }}
