{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "dfuchs-test.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "dfuchs-test.labels" -}}
helm.sh/chart: {{ include "dfuchs-test.chart" . }}
{{ include "dfuchs-test.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "dfuchs-test.selectorLabels" -}}
app.kubernetes.io/name: "dfuchs-test"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
