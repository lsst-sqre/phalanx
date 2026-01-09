{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "muster.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "muster.labels" -}}
helm.sh/chart: {{ include "muster.chart" . }}
{{ include "muster.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "muster.selectorLabels" -}}
app.kubernetes.io/name: "muster"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
