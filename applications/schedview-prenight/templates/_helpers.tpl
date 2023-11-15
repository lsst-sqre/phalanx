{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "schedview-prenight.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "schedview-prenight.labels" -}}
helm.sh/chart: {{ include "schedview-prenight.chart" . }}
{{ include "schedview-prenight.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "schedview-prenight.selectorLabels" -}}
app.kubernetes.io/name: "schedview-prenight"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
