{{/*
Expand the name of the chart.
*/}}
{{- define "cadc-tap.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "cadc-tap.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "cadc-tap.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Common labels
*/}}
{{- define "cadc-tap.labels" -}}
app.kubernetes.io/name: {{ include "cadc-tap.name" . }}
helm.sh/chart: {{ include "cadc-tap.chart" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

{{/*
Selector labels
*/}}
{{- define "cadc-tap.selectorLabels" -}}
app.kubernetes.io/name: {{ include "cadc-tap.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Validate the configured data backend is one of the allowed values.
*/}}
{{- define "cadc-tap.validateBackend" -}}
  {{- $validBackends := list "pg" "qserv" "bigquery" -}}
  {{- if not (has .Values.config.backend $validBackends) -}}
    {{- fail (printf "config.backend must be set to one of: %s (got '%s')" (join ", " $validBackends) .Values.config.backend) -}}
  {{- end -}}
{{- end -}}

{{/*
Validate database type is one of the allowed values.
*/}}
{{- define "cadc-tap.validateDatabaseType" -}}
  {{- $validTypes := list "containerized" "cloudsql" "external" -}}
  {{- $type := . -}}
  {{- if not (has $type $validTypes) -}}
    {{- fail (printf "Invalid database type '%s'. Must be one of: %s" $type (join ", " $validTypes)) -}}
  {{- end -}}
{{- end -}}

{{/*
Generate Cloud SQL proxy init container if needed.
*/}}
{{- define "cadc-tap.cloudSqlProxyContainer" -}}
{{- if or .Values.cloudsql.enabled (eq .Values.tapSchema.type "cloudsql") (eq .Values.uws.type "cloudsql") }}
- name: "cloud-sql-proxy"
  command:
    - "/cloud_sql_proxy"
    - "-ip_address_types=PRIVATE"
    - "-log_debug_stdout=true"
    - "-structured_logs=true"
    - "-instances={{ required "cloudsql.instanceConnectionName must be specified" .Values.cloudsql.instanceConnectionName }}=tcp:5432"
  image: "{{ .Values.cloudsql.image.repository }}:{{ .Values.cloudsql.image.tag }}"
  imagePullPolicy: {{ .Values.cloudsql.image.pullPolicy | quote }}
  {{- with .Values.cloudsql.resources }}
  resources:
    {{- toYaml . | nindent 4 }}
  {{- end }}
  restartPolicy: "Always"
  securityContext:
    allowPrivilegeEscalation: false
    capabilities:
      drop:
        - "all"
    readOnlyRootFilesystem: true
    runAsNonRoot: true
    runAsUser: 65532
    runAsGroup: 65532
{{- end }}
{{- end }}
