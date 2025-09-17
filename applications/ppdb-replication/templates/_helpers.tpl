{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "ppdb-replication.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "ppdb-replication.labels" -}}
helm.sh/chart: {{ include "ppdb-replication.chart" . }}
{{ include "ppdb-replication.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "ppdb-replication.selectorLabels" -}}
app.kubernetes.io/name: "ppdb-replication"
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "ppdb-replication.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{- define "ppdb-replication.deployment" -}}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "ppdb-replication.fullname" . }}-{{ .containerSuffix }}
  labels:
    {{- include "ppdb-replication.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "ppdb-replication.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "ppdb-replication.selectorLabels" . | nindent 8 }}
      annotations:
        checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
        {{- with .Values.podAnnotations }}
        {{- toYaml . | nindent 8 }}
        {{- end }}
    spec:
      volumes:
        - name: "ppdb-replication-secrets-raw"
          secret:
            secretName: {{ include "ppdb-replication.fullname" . }}
        - name: "ppdb-replication-secrets"
          emptyDir:
            sizeLimit: "100Mi"
        {{- with .Values.config.volumes }}
        {{- . | toYaml | nindent 8 }}
        {{- end }}
      initContainers:
        - name: fix-secret-permissions
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          imagePullPolicy: {{ .Values.image.pullPolicy | quote }}
          command:
            - "/bin/sh"
            - "-c"
            - |
              cp -RL /tmp/ppdb-replication-secrets-raw/* /app/secrets/
              chown 8286:4085 /app/secrets/*
              chmod 0400 /app/secrets/*
          securityContext:
            runAsNonRoot: false
            runAsUser: 0
            runAsGroup: 0
          volumeMounts:
            - name: "ppdb-replication-secrets"
              mountPath: "/app/secrets"
            - name: "ppdb-replication-secrets-raw"
              mountPath: "/tmp/ppdb-replication-secrets-raw"
              readOnly: true
      containers:
        - name: "{{ .Chart.Name }}-{{ .containerSuffix }}"
          envFrom:
            - configMapRef:
                name: "ppdb-replication"
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          env:
            - name: AWS_SHARED_CREDENTIALS_FILE
              value: "/app/secrets/aws-credentials.ini"
            - name: PGPASSFILE
              value: "/app/secrets/postgres-credentials.txt"
            - name: LSST_DB_AUTH
              value: "/app/secrets/db-auth.yaml"
            - name: S3_ENDPOINT_URL
              value: {{ .Values.config.s3EndpointUrl | quote }}
            - name: LSST_RESOURCES_S3_PROFILE_{{ .Values.config.additionalS3ProfileName }}
              value: {{ .Values.config.additionalS3ProfileUrl | quote }}
            - name: LSST_DISABLE_BUCKET_VALIDATION
              value: {{ .Values.config.disableBucketValidation | quote }}
            - name: GOOGLE_APPLICATION_CREDENTIALS
              value: "/app/secrets/gcs-credentials.json"
          volumeMounts:
            - name: "ppdb-replication-secrets"
              mountPath: "/app/secrets"
              readOnly: true
            {{- with .Values.config.volumeMounts }}
            {{- . | toYaml | nindent 12 }}
            {{- end }}
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
          args:
            {{- range .containerArgs }}
            - {{ . | quote }}
            {{- end }}
      securityContext:
        runAsNonRoot: true
        runAsUser: 8286
        runAsGroup: 4085
        fsGroup: 4085
      {{- with .Values.nodeSelector }}
      nodeSelector:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.tolerations }}
      tolerations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
{{- end }}
