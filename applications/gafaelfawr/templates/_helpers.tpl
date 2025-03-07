{{/* vim: set filetype=mustache: */}}
{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "gafaelfawr.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "gafaelfawr.labels" -}}
helm.sh/chart: {{ include "gafaelfawr.chart" . }}
{{ include "gafaelfawr.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "gafaelfawr.selectorLabels" -}}
app.kubernetes.io/name: "gafaelfawr"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Cloud SQL Auth Proxy sidecar container
*/}}
{{- define "gafaelfawr.cloudsqlSidecar" -}}
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
    {{- toYaml . | nindent 12 }}
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

{{/*
Common environment variables
*/}}
{{- define "gafaelfawr.envVars" -}}
{{- if (not .Values.config.afterLogoutUrl) }}
- name: "GAFAELFAWR_AFTER_LOGOUT_URL"
  value: {{ required "global.baseUrl must be set" .Values.global.baseUrl | quote }}
{{- end }}
- name: "GAFAELFAWR_BASE_URL"
  value: {{ .Values.global.baseUrl | quote }}
{{- if not .Values.config.baseInternalUrl }}
- name: "GAFAELFAWR_BASE_INTERNAL_URL"
  value: "http://gafaelfawr.{{ .Release.Namespace }}.svc.cluster.local:8080"
{{- end }}
- name: "GAFAELFAWR_BOOTSTRAP_TOKEN"
  valueFrom:
    secretKeyRef:
      name: "gafaelfawr"
      key: "bootstrap-token"
{{- if .Values.config.cilogon.clientId }}
- name: "GAFAELFAWR_CILOGON_CLIENT_SECRET"
  valueFrom:
    secretKeyRef:
      name: "gafaelfawr"
      key: "cilogon-client-secret"
{{- end }}
- name: "GAFAELFAWR_DATABASE_PASSWORD"
  valueFrom:
    secretKeyRef:
      name: "gafaelfawr"
      key: "database-password"
{{- if (or .Values.cloudsql.enabled .Values.config.internalDatabase) }}
- name: "GAFAELFAWR_DATABASE_URL"
  {{- if (and .sidecar .Values.cloudsql.enabled) }}
  value: "postgresql://gafaelfawr@localhost/gafaelfawr"
  {{- else if .Values.cloudsql.enabled }}
  value: "postgresql://gafaelfawr@cloud-sql-proxy/gafaelfawr"
  {{- else if .Values.config.internalDatabase }}
  value: "postgresql://gafaelfawr@postgres.postgres/gafaelfawr"
  {{- end }}
{{- end }}
{{- if .Values.config.github.clientId }}
- name: "GAFAELFAWR_GITHUB_CLIENT_SECRET"
  valueFrom:
    secretKeyRef:
      name: "gafaelfawr"
      key: "github-client-secret"
{{- end }}
{{- if .Values.config.ldap.userDn }}
- name: "GAFAELFAWR_LDAP_PASSWORD"
  valueFrom:
    secretKeyRef:
      name: "gafaelfawr"
      key: "ldap-password"
{{- end }}
{{- if .Values.config.oidc.clientId }}
- name: "GAFAELFAWR_OIDC_CLIENT_SECRET"
  valueFrom:
    secretKeyRef:
      name: "gafaelfawr"
      key: "oidc-client-secret"
{{- end }}
{{- if .Values.config.oidcServer.enabled }}
- name: "GAFAELFAWR_OIDC_SERVER_CLIENTS"
  valueFrom:
    secretKeyRef:
      name: "gafaelfawr"
      key: "oidc-server-secrets"
{{- if (not .Values.config.oidcServer.issuer) }}
- name: "GAFAELFAWR_OIDC_SERVER_ISSUER"
  value: {{ .Values.global.baseUrl | quote }}
{{- end }}
- name: "GAFAELFAWR_OIDC_SERVER_KEY"
  valueFrom:
    secretKeyRef:
      name: "gafaelfawr"
      key: "signing-key"
{{- end }}
{{- if (not .Values.config.realm) }}
- name: "GAFAELFAWR_REALM"
  value: {{ required "global.host must be set" .Values.global.host | quote }}
{{- end }}
- name: "GAFAELFAWR_REDIRECT_URL"
  value: "{{ .Values.global.baseUrl }}/login"
- name: "GAFAELFAWR_REDIS_PASSWORD"
  valueFrom:
    secretKeyRef:
      name: "gafaelfawr"
      key: "redis-password"
- name: "GAFAELFAWR_REDIS_EPHEMERAL_URL"
  value: "redis://gafaelfawr-redis-ephemeral.{{ .Release.Namespace }}:6379/0"
- name: "GAFAELFAWR_REDIS_PERSISTENT_URL"
  value: "redis://gafaelfawr-redis.{{ .Release.Namespace }}:6379/0"
- name: "GAFAELFAWR_SESSION_SECRET"
  valueFrom:
    secretKeyRef:
      name: "gafaelfawr"
      key: "session-secret"
{{- if .Values.config.slackAlerts }}
- name: "GAFAELFAWR_SLACK_WEBHOOK"
  valueFrom:
    secretKeyRef:
      name: "gafaelfawr"
      key: "slack-webhook"
{{- end }}
{{- if .Values.config.metrics.enabled }}
- name: "KAFKA_BOOTSTRAP_SERVERS"
  valueFrom:
    secretKeyRef:
      name: "gafaelfawr-kafka"
      key: "bootstrapServers"
- name: "KAFKA_SECURITY_PROTOCOL"
  valueFrom:
    secretKeyRef:
      name: "gafaelfawr-kafka"
      key: "securityProtocol"
{{- end }}
{{- if .Values.config.enableSentry }}
- name: SENTRY_DSN
  valueFrom:
    secretKeyRef:
      name: "gafaelfawr"
      key: "sentry-dsn"
- name: SENTRY_RELEASE
  value: {{ .Chart.Name }}@{{ .Chart.AppVersion }}
- name: SENTRY_ENVIRONMENT
  value: {{ .Values.global.host }}
{{- end }}
{{- end }}
