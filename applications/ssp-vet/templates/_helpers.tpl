{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "ssp-vet.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "ssp-vet.labels" -}}
helm.sh/chart: {{ include "ssp-vet.chart" . }}
{{ include "ssp-vet.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "ssp-vet.selectorLabels" -}}
app.kubernetes.io/name: "ssp-vet"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
