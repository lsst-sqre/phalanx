{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "jira-stats.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "jira-stats.labels" -}}
helm.sh/chart: {{ include "jira-stats.chart" . }}
{{ include "jira-stats.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "jira-stats.selectorLabels" -}}
app.kubernetes.io/name: "jira-stats"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
