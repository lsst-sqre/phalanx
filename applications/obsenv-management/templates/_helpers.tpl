{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "obsenv-management.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "obsenv-management.labels" -}}
helm.sh/chart: {{ include "obsenv-management.chart" . }}
{{ include "obsenv-management.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "obsenv-management.selectorLabels" -}}
app.kubernetes.io/name: "obsenv-management"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
