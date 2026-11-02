{{- define "integration-testing.volumes" -}}
volumes:
- name: testreports
  persistentVolumeClaim:
    claimName: {{ .Values.persistentVolume.claimName }}
{{- if .Values.efdCredentials }}
- name: efd-credentials-raw
  secret:
    secretName: control-system-test
    items:
    - key: {{ .Values.efdCredentials.secretFilename }}
      path: {{ .Values.efdCredentials.secretFilename }}
    defaultMode: 0440
- name: efd-credentials
  emptyDir: {}
{{- end }}
{{- end }}