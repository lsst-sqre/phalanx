{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "opensearch-cluster.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "opensearch-cluster.labels" -}}
helm.sh/chart: {{ include "opensearch-cluster.chart" . }}
{{ include "opensearch-cluster.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "opensearch-cluster.selectorLabels" -}}
app.kubernetes.io/name: "opensearch-cluster"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
