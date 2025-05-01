{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "victoria-metrics-k8s.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "victoria-metrics-k8s.labels" -}}
helm.sh/chart: {{ include "victoria-metrics-k8s.chart" . }}
{{ include "victoria-metrics-k8s.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "victoria-metrics-k8s.selectorLabels" -}}
app.kubernetes.io/name: "victoria-metrics-k8s"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
