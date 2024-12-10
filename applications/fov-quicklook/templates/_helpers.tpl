{{- define "fov-quicklook.env.s3_tile" -}}
- name: QUICKLOOK_s3_tile
  value: {{ .Values.s3_tile | toJson | quote }}
- name: QUICKLOOK_s3_tile__access_key
  valueFrom:
    secretKeyRef:
      name: fov-quicklook
      key: s3_tile_access_key
- name: QUICKLOOK_s3_tile__secret_key
  valueFrom:
    secretKeyRef:
      name: fov-quicklook
      key: s3_tile_secret_key
{{- end }}

{{- define "fov-quicklook.env.s3_repository" -}}
- name: QUICKLOOK_s3_repository
  value: {{ .Values.s3_repository | toJson | quote }}
- name: QUICKLOOK_s3_repository__access_key
  valueFrom:
    secretKeyRef:
      name: fov-quicklook
      key: s3_repository_access_key
- name: QUICKLOOK_s3_repository__secret_key
  valueFrom:
    secretKeyRef:
      name: fov-quicklook
      key: s3_repository_secret_key
{{- end }}

{{- define "quicklook.ingress.spec" -}}
rules:
  - http:
      paths:
        - path: {{ .Values.config.pathPrefix }}
          pathType: Prefix
          backend:
            service:
              name: fov-quicklook-frontend
              port:
                number: 9500
{{- end -}}

{{- define "quicklook.butler-settings.env" -}}
- name: AWS_SHARED_CREDENTIALS_FILE
  value: /var/run/secrets/aws-credentials.ini
- name: PGPASSFILE
  value: /var/run/secrets/postgres-credentials.txt
- name: PGUSER
  value: rubin
- name: LSST_RESOURCES_S3_PROFILE_embargo
  value: https://sdfembs3.sdf.slac.stanford.edu
- name: DAF_BUTLER_REPOSITORY_INDEX
  value: s3://embargo@rubin-summit-users/data-repos.yaml
{{- end -}}

{{- define "quicklook.butler-settings.volumes" -}}
- name: butler-settings
  secret:
    secretName: fov-quicklook
{{- end -}}

{{- define "quicklook.butler-settings.volumeMounts" -}}
- name: butler-settings
  mountPath: /var/run/secrets/aws-credentials.ini
  subPath: aws-credentials.ini
- name: butler-settings
  mountPath: /var/run/secrets/postgres-credentials.txt
  subPath: postgres-credentials.txt
{{- end -}}
