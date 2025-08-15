{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "strimzi-registry-operator.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "strimzi-registry-operator.labels" -}}
helm.sh/chart: {{ include "strimzi-registry-operator.chart" . }}
{{ include "strimzi-registry-operator.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "strimzi-registry-operator.selectorLabels" -}}
app.kubernetes.io/name: "strimzi-registry-operator"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
