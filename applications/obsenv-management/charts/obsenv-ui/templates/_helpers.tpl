{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "obsenv-ui.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "obsenv-ui.labels" -}}
helm.sh/chart: {{ include "obsenv-ui.chart" . }}
{{ include "obsenv-ui.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "obsenv-ui.selectorLabels" -}}
app.kubernetes.io/name: "obsenv-ui"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
