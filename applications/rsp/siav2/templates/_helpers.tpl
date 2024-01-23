{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "siav2.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "siav2.labels" -}}
helm.sh/chart: {{ include "siav2.chart" . }}
{{ include "siav2.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "siav2.selectorLabels" -}}
app.kubernetes.io/name: "siav2"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
