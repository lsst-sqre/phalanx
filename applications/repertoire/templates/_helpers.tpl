{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "repertoire.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "repertoire.labels" -}}
helm.sh/chart: {{ include "repertoire.chart" . }}
{{ include "repertoire.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "repertoire.selectorLabels" -}}
app.kubernetes.io/name: "repertoire"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
