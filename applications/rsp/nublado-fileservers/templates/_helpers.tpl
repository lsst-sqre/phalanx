{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "nublado-fileservers.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "nublado-fileservers.labels" -}}
helm.sh/chart: {{ include "nublado-fileservers.chart" . }}
{{ include "nublado-fileservers.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "nublado-fileservers.selectorLabels" -}}
app.kubernetes.io/name: "nublado-fileservers"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
