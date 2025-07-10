{{/* Shared spec for init-output Job and CronJob. */}}
{{- define "prompt-keda.service-init" -}}
spec:
  template:
    metadata:
      {{- with .Values.initializer.podAnnotations }}
      annotations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
    spec:
      initContainers:
      {{- include "prompt-keda.dbauth-initcontainer" . | nindent 6 }}
      containers:
      - image: "{{ .Values.initializer.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
        imagePullPolicy: {{ .Values.image.pullPolicy | quote }}
        name: {{ include "prompt-keda.fullname" . | trimPrefix "prompt-keda-" }}
        env:
        - name: RUBIN_INSTRUMENT
          value: {{ .Values.instrument.name }}
        - name: PREPROCESSING_PIPELINES_CONFIG
          value: |-
            {{- .Values.instrument.pipelines.preprocessing | nindent 12 }}
        - name: MAIN_PIPELINES_CONFIG
          value: |-
            {{- .Values.instrument.pipelines.main | nindent 12 }}
        - name: EXPORT_TYPE_REGEXP
          value: {{- toYaml .Values.instrument.exportTypes | nindent 12 }}
        - name: SKYMAP
          value: {{ .Values.instrument.skymap }}
        - name: CENTRAL_REPO
          value: {{ .Values.instrument.centralRepo }}
        - name: REPO_RETRY_DELAY
          value: {{ .Values.instrument.repoWait | toString | quote }}
        - name: LSST_DISABLE_BUCKET_VALIDATION
          value: {{ .Values.s3.disableBucketValidation | toString | quote }}
        - name: CONFIG_APDB
          value: {{ .Values.apdb.config }}
        {{- with .Values.iers_cache }}
        - name: CENTRAL_IERS_CACHE
          value: {{ . }}
        {{- end }}
        {{- with .Values.sattle.uri_base }}
        - name: SATTLE_URI_BASE
          value: {{ . }}
        {{- end }}
        - name: SASQUATCH_URL
          value: {{ .Values.sasquatch.endpointUrl }}
        {{- if and .Values.sasquatch.endpointUrl .Values.sasquatch.auth_env }}
        - name: SASQUATCH_TOKEN
          valueFrom:
            secretKeyRef:
              name: {{ template "prompt-keda.fullname" . }}-secret
              key: sasquatch_token
        {{- end }}
        - name: DAF_BUTLER_SASQUATCH_NAMESPACE
          value: {{ .Values.sasquatch.namespace }}
        {{- include "prompt-keda.s3-env" . | nindent 8 }}
        {{- include "prompt-keda.db-auth-env" . | nindent 8 }}
        {{- /* Job does not produce alerts, but PackageAlertsTask may ping the server. */}}
        - name: AP_KAFKA_PRODUCER_PASSWORD
          valueFrom:
            secretKeyRef:
              name: {{ template "prompt-keda.fullname" . }}-secret
              key: alert_stream_pass
        - name: AP_KAFKA_PRODUCER_USERNAME
          value: {{ .Values.alerts.username}}
        - name: AP_KAFKA_SERVER
          value: {{ .Values.alerts.server}}
        - name: AP_KAFKA_TOPIC
          value: {{ .Values.alerts.topic}}
        - name: SERVICE_LOG_LEVELS
          value: {{ .Values.logLevel }}
        volumeMounts:
        {{- include "prompt-keda.credentials-volumeMounts" . | nindent 8 }}
        {{- if .Values.registry.centralRepoFile }}
        - mountPath: {{ .Values.instrument.centralRepo }}
          name: central-repo-file
        {{- end }}
        {{- with .Values.additionalVolumeMounts }}
        {{- toYaml . | nindent 8 }}
        {{- end }}
        resources:
          requests:
            cpu: {{ .Values.initializer.resources.cpuRequest | toString | quote}}
            memory: {{ .Values.initializer.resources.memoryRequest }}
          limits:
            cpu: {{ .Values.initializer.resources.cpuLimit | toString | quote}}
            memory: {{ .Values.initializer.resources.memoryLimit }}
      volumes:
      {{- include "prompt-keda.credentials-volumes" . | nindent 6 }}
      {{- if .Values.registry.centralRepoFile }}
      - name: central-repo-file
        secret:
          secretName: {{ template "prompt-keda.fullname" . }}-secret
          items:
          - key: central_repo_file
            path: butler.yaml
      {{- end }}
      {{- with .Values.tolerations }}
      tolerations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.affinity }}
      affinity:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      enableServiceLinks: true
      restartPolicy: Never
      activeDeadlineSeconds: {{ .Values.initializer.timeout }}
  backoffLimit: {{ .Values.initializer.retries }}
  ttlSecondsAfterFinished: {{ .Values.initializer.cleanup_delay }}
  podFailurePolicy:
    rules:
    # Successful init is essential for other components, don't fail on external shutdowns
    - action: Ignore
      onPodConditions:
      - type: DisruptionTarget
        status: "True"
{{- end }}
