{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "gke.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "gke.labels" -}}
helm.sh/chart: {{ include "gke.chart" . }}
{{ include "gke.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "gke.selectorLabels" -}}
app.kubernetes.io/name: "gke"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
