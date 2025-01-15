{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "tasso.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "tasso.labels" -}}
helm.sh/chart: {{ include "tasso.chart" . }}
{{ include "tasso.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "tasso.selectorLabels" -}}
app.kubernetes.io/name: "tasso"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
