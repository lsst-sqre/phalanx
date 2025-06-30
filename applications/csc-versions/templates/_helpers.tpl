{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "csc-versions.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "csc-versions.labels" -}}
helm.sh/chart: {{ include "csc-versions.chart" . }}
{{ include "csc-versions.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "csc-versions.selectorLabels" -}}
app.kubernetes.io/name: "csc-versions"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
