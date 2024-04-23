{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "consdb.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "consdb.labels" -}}
helm.sh/chart: {{ include "consdb.chart" . }}
{{ include "consdb.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "consdb.selectorLabels" -}}
app.kubernetes.io/name: "consdb"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
