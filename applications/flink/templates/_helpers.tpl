{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "flink.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "flink.labels" -}}
helm.sh/chart: {{ include "flink.chart" . }}
{{ include "flink.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "flink.selectorLabels" -}}
app.kubernetes.io/name: "flink"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
