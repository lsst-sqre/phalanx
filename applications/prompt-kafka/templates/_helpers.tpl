{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "prompt-kafka.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "prompt-kafka.labels" -}}
helm.sh/chart: {{ include "prompt-kafka.chart" . }}
{{ include "prompt-kafka.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "prompt-kafka.selectorLabels" -}}
app.kubernetes.io/name: "prompt-kafka"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
