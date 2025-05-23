{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "google-cloud-observability.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "google-cloud-observability.labels" -}}
helm.sh/chart: {{ include "google-cloud-observability.chart" . }}
{{ include "google-cloud-observability.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "google-cloud-observability.selectorLabels" -}}
app.kubernetes.io/name: "google-cloud-observability"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
