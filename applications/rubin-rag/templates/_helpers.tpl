{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "rubin-rag.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "rubin-rag.labels" -}}
helm.sh/chart: {{ include "rubin-rag.chart" . }}
{{ include "rubin-rag.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "rubin-rag.selectorLabels" -}}
app.kubernetes.io/name: "rubin-rag"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
