{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "schedview-static-pages.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "schedview-static-pages.labels" -}}
helm.sh/chart: {{ include "schedview-static-pages.chart" . }}
{{ include "schedview-static-pages.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "schedview-static-pages.selectorLabels" -}}
app.kubernetes.io/name: "schedview-static-pages"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
