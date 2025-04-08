{{/* Shared spec for init-output Job and CronJob. */}}
{{- define "prompt-proto-service.service-init" -}}
spec:
  template:
    metadata:
      {{- with .Values.initializer.podAnnotations }}
      annotations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
    spec:
      initContainers:
      - name: init-db-auth
        # Make a copy of the read-only secret that's owned by lsst
        # lsst account is created by main image with id 1000
        image: busybox
        command: ["sh", "-c", "cp -L /app/db-auth-mount/db-auth.yaml /app/dbauth/ && chown 1000:1000 /app/dbauth/db-auth.yaml && chmod u=r,go-rwx /app/dbauth/db-auth.yaml"]
        volumeMounts:
        - mountPath: /app/db-auth-mount
          name: db-auth-mount
          readOnly: true
        - mountPath: /app/dbauth
          name: db-auth-credentials-file
      containers:
      - image: "{{ .Values.initializer.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
        imagePullPolicy: {{ .Values.image.pullPolicy | quote }}
        name: user-container
        env:
        - name: RUBIN_INSTRUMENT
          value: {{ .Values.instrument.name }}
        - name: PREPROCESSING_PIPELINES_CONFIG
          value: |-
            {{- .Values.instrument.pipelines.preprocessing | nindent 12 }}
        - name: MAIN_PIPELINES_CONFIG
          value: |-
            {{- .Values.instrument.pipelines.main | nindent 12 }}
        - name: SKYMAP
          value: {{ .Values.instrument.skymap }}
        - name: CALIB_REPO
          value: {{ .Values.instrument.calibRepo }}
        - name: LSST_DISABLE_BUCKET_VALIDATION
          value: {{ .Values.s3.disableBucketValidation | toString | quote }}
        - name: CONFIG_APDB
          value: {{ .Values.apdb.config }}
        - name: SASQUATCH_URL
          value: {{ .Values.sasquatch.endpointUrl }}
        {{- if and .Values.sasquatch.endpointUrl .Values.sasquatch.auth_env }}
        - name: SASQUATCH_TOKEN
          valueFrom:
            secretKeyRef:
              name: {{ template "prompt-proto-service.fullname" . }}-secret
              key: sasquatch_token
        {{- end }}
        - name: DAF_BUTLER_SASQUATCH_NAMESPACE
          value: {{ .Values.sasquatch.namespace }}
        - name: S3_ENDPOINT_URL
          value: {{ .Values.s3.endpointUrl }}
        {{- if .Values.s3.auth_env }}
        - name: AWS_ACCESS_KEY_ID
          valueFrom:
            secretKeyRef:
              name: {{ template "prompt-proto-service.fullname" . }}-secret
              key: s3_access_key
        - name: AWS_SECRET_ACCESS_KEY
          valueFrom:
            secretKeyRef:
              name: {{ template "prompt-proto-service.fullname" . }}-secret
              key: s3_secret_key
        {{- end }}
        {{- if .Values.s3.cred_file_auth }}
        - name: AWS_SHARED_CREDENTIALS_FILE
          value: /app/s3/credentials
        {{- end }}
        {{- with .Values.s3.aws_profile }}
        - name: AWS_PROFILE
          value: {{ . }}
        {{- end }}
        {{- with .Values.s3.checksum }}
        - name: AWS_REQUEST_CHECKSUM_CALCULATION
          value: {{ . }}
        {{- end }}
        - name: LSST_DB_AUTH
          value: /app/lsst-credentials/db-auth.yaml
        {{- /* Job does not produce alerts, but PackageAlertsTask may ping the server. */}}
        - name: AP_KAFKA_PRODUCER_PASSWORD
          valueFrom:
            secretKeyRef:
              name: {{ template "prompt-proto-service.fullname" . }}-secret
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
        - mountPath: /app/lsst-credentials
          name: db-auth-credentials-file
          readOnly: true
        {{- if .Values.s3.cred_file_auth }}
        - mountPath: /app/s3/
          name: s3-credentials-file
        {{- end }}
        {{- if .Values.registry.centralRepoFile }}
        - mountPath: {{ .Values.instrument.calibRepo }}
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
      - name: db-auth-mount
        # Temporary mount for db-auth.yaml; cannot be read directly because it's owned by root
        secret:
          secretName: {{ template "prompt-proto-service.fullname" . }}-secret
          defaultMode: 256
          items:
            - key: db-auth_file
              path: db-auth.yaml
      - name: db-auth-credentials-file
        emptyDir:
          sizeLimit: 10Ki  # Just a text file!
      {{- if .Values.s3.cred_file_auth }}
      - name: s3-credentials-file
        secret:
          secretName: {{ template "prompt-proto-service.fullname" . }}-secret
          items:
           - key: s3_credentials_file
             path: credentials
      {{- end }}
      {{- if .Values.registry.centralRepoFile }}
      - name: central-repo-file
        secret:
          secretName: {{ template "prompt-proto-service.fullname" . }}-secret
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
