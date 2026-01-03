{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "octavius.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}


{{/*
Create a default fully qualified app name.
*/}}
{{- define "octavius.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}


{{/*
Common labels
*/}}
{{- define "octavius.labels" -}}
helm.sh/chart: {{ include "octavius.chart" . }}
{{ include "octavius.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "octavius.selectorLabels" -}}
app.kubernetes.io/name: "octavius"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
