{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "schedview_prenight.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "schedview_prenight.labels" -}}
helm.sh/chart: {{ include "schedview_prenight.chart" . }}
{{ include "schedview_prenight.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "schedview_prenight.selectorLabels" -}}
app.kubernetes.io/name: "schedview_prenight"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
