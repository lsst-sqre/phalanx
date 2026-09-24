{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "so-evening-tailgate.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "so-evening-tailgate.labels" -}}
helm.sh/chart: {{ include "so-evening-tailgate.chart" . }}
{{ include "so-evening-tailgate.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "so-evening-tailgate.selectorLabels" -}}
app.kubernetes.io/name: "so-evening-tailgate"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
