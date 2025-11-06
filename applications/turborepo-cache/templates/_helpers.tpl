{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "turborepo-cache.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "turborepo-cache.labels" -}}
helm.sh/chart: {{ include "turborepo-cache.chart" . }}
{{ include "turborepo-cache.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "turborepo-cache.selectorLabels" -}}
app.kubernetes.io/name: "turborepo-cache"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Cache component labels
*/}}
{{- define "turborepo-cache.cache.labels" -}}
helm.sh/chart: {{ include "turborepo-cache.chart" . }}
{{ include "turborepo-cache.cache.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Cache component selector labels
*/}}
{{- define "turborepo-cache.cache.selectorLabels" -}}
app.kubernetes.io/name: "turborepo-cache"
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/component: "cache"
{{- end }}

{{/*
Proxy component labels
*/}}
{{- define "turborepo-cache.proxy.labels" -}}
helm.sh/chart: {{ include "turborepo-cache.chart" . }}
{{ include "turborepo-cache.proxy.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Proxy component selector labels
*/}}
{{- define "turborepo-cache.proxy.selectorLabels" -}}
app.kubernetes.io/name: "turborepo-cache"
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/component: "proxy"
{{- end }}
