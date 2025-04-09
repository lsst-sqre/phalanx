{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "qserv-kafka.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "qserv-kafka.labels" -}}
helm.sh/chart: {{ include "qserv-kafka.chart" . }}
{{ include "qserv-kafka.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "qserv-kafka.selectorLabels" -}}
app.kubernetes.io/name: "qserv-kafka"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
