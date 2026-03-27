{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "prompt-pub.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "prompt-pub.labels" -}}
helm.sh/chart: {{ include "prompt-pub.chart" . }}
{{ include "prompt-pub.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "prompt-pub.selectorLabels" -}}
app.kubernetes.io/name: "prompt-pub"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
