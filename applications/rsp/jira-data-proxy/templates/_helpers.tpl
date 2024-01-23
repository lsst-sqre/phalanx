{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "jira-data-proxy.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "jira-data-proxy.labels" -}}
helm.sh/chart: {{ include "jira-data-proxy.chart" . }}
{{ include "jira-data-proxy.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "jira-data-proxy.selectorLabels" -}}
app.kubernetes.io/name: "jira-data-proxy"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
