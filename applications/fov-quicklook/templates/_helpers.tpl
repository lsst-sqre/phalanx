{{- define "fov-quicklook.env.s3_tile" -}}
- name: QUICKLOOK_s3_tile
  value: {{ .Values.s3_tile | toJson | quote }}
- name: QUICKLOOK_s3_tile__access_key
  valueFrom:
    secretKeyRef:
      name: fov-quicklook-secret
      key: s3_tile_access_key
- name: QUICKLOOK_s3_tile__secret_key
  valueFrom:
    secretKeyRef:
      name: fov-quicklook-secret
      key: s3_tile_secret_key
{{- end }}

{{- define "fov-quicklook.env.s3_repository" -}}
- name: QUICKLOOK_s3_repository
  value: {{ .Values.s3_repository | toJson | quote }}
- name: QUICKLOOK_s3_repository__access_key
  valueFrom:
    secretKeyRef:
      name: fov-quicklook-secret
      key: s3_repository_aceess_key
- name: QUICKLOOK_s3_repository__secret_key
  valueFrom:
    secretKeyRef:
      name: fov-quicklook-secret
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
              name: quicklook-frontend
              port:
                number: 9500
{{- end -}}
