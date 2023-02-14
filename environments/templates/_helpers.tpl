{{/* vim: set filetype=mustache: */}}
{{- define "enabledServices" -}}
argocd
  {{- range $okey, $oval := .Values }}
    {{- $otype := typeOf $oval -}}
      {{- if eq $otype  "map[string]interface {}" }}
        {{- if hasKey $oval "enabled" }}
{{- if $oval.enabled }}@{{- $okey }}{{- end }}
      {{- end }}
    {{- end }}
  {{- end }}
{{- end }}
