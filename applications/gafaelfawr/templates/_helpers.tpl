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
- name: "GAFAELFAWR_CILOGON__CLIENT_SECRET"
  valueFrom:
    secretKeyRef:
      name: "gafaelfawr"
      key: "cilogon-client-secret"
{{- end }}
- name: "GAFAELFAWR_CILOGON__REDIRECT_URL"
  value: "{{ .Values.global.baseUrl }}/login"
{{- if eq .Values.config.database.type "external" }}
- name: "GAFAELFAWR_DATABASE__PASSWORD"
  valueFrom:
    secretKeyRef:
      name: "gafaelfawr"
      key: "database-password"
{{- end }}
{{- if .Values.config.internalDatabase }}
- name: "GAFAELFAWR_DATABASE__URL"
  value: "postgresql://gafaelfawr@postgres.postgres/gafaelfawr"
{{- end }}
{{- if .Values.config.github.clientId }}
- name: "GAFAELFAWR_GITHUB__CLIENT_SECRET"
  valueFrom:
    secretKeyRef:
      name: "gafaelfawr"
      key: "github-client-secret"
{{- end }}
{{- if .Values.config.ldap.userDn }}
- name: "GAFAELFAWR_LDAP__PASSWORD"
  valueFrom:
    secretKeyRef:
      name: "gafaelfawr"
      key: "ldap-password"
{{- end }}
{{- if .Values.config.oidc.clientId }}
- name: "GAFAELFAWR_OIDC__CLIENT_SECRET"
  valueFrom:
    secretKeyRef:
      name: "gafaelfawr"
      key: "oidc-client-secret"
{{- end }}
- name: "GAFAELFAWR_OIDC__REDIRECT_URL"
  value: "{{ .Values.global.baseUrl }}/login"
{{- if .Values.config.oidcServer.enabled }}
- name: "GAFAELFAWR_OIDC_SERVER__CLIENTS"
  valueFrom:
    secretKeyRef:
      name: "gafaelfawr"
      key: "oidc-server-secrets"
{{- if (not .Values.config.oidcServer.issuer) }}
- name: "GAFAELFAWR_OIDC_SERVER__CLIENT_SUFFIX"
  value: ".clients.{{ .Values.global.host }}"
- name: "GAFAELFAWR_OIDC_SERVER__ISSUER"
  value: {{ .Values.global.baseUrl | quote }}
{{- end }}
- name: "GAFAELFAWR_OIDC_SERVER__KEY"
  valueFrom:
    secretKeyRef:
      name: "gafaelfawr"
      key: "signing-key"
{{- end }}
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
{{- if .Values.config.sentry.enabled }}
- name: "SENTRY_DSN"
  valueFrom:
    secretKeyRef:
      name: "gafaelfawr"
      key: "sentry-dsn"
- name: "SENTRY_ENVIRONMENT"
  value: {{ .Values.global.environmentName | quote }}
- name: "SENTRY_TRACES_SAMPLE_RATE"
  value: {{ .Values.config.sentry.tracesSampleRate | quote }}
{{- end }}
{{- end }}
