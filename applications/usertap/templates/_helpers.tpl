{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "usertap.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "usertap.labels" -}}
helm.sh/chart: {{ include "usertap.chart" . }}
{{ include "usertap.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "usertap.selectorLabels" -}}
app.kubernetes.io/name: "usertap"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
