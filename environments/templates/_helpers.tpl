{{/* vim: set filetype=mustache: */}}
{{- define "enabledServices" -}}
  {{- range $app, $enabled := .Values.applications }}
    {{- if $enabled }}@{{ $app }}{{ end }}
  {{- end }}
{{- end }}

{{- define "enabledServicesYamlList" }}
{{- range $app, $enabled := .Values.applications }}
  {{- if $enabled }}
- {{ $app | quote }}
  {{- end }}
{{- end }}
{{- end -}}
