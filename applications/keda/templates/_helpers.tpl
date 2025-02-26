{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "keda.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "keda.labels" }}
helm.sh/chart: {{ include "keda.chart" . }}
{{ include "keda.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "keda.selectorLabels" -}}
app.kubernetes.io/name: "keda"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
