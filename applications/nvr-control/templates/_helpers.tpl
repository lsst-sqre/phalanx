{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "nvr-control.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "nvr-control.labels" -}}
helm.sh/chart: {{ include "nvr-control.chart" . }}
{{ include "nvr-control.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "nvr-control.selectorLabels" -}}
app.kubernetes.io/name: nvr-control
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
