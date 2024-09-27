{{/* Define a helper to get the current timestamp */}}
{{- define "getCurrentTimestamp" -}}
{{- now | date "20060102150405" }}
{{- end -}}

{{- /*
Generate a base name for resources using only the chart name or nameOverride if provided.
Does not include the release name.
*/ -}}
{{- define "prefect.fullname" -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- $fullname := printf "%s" $name | trunc 63 | trimSuffix "-" -}}
{{- $fullname | replace "_" "-" | lower -}}
{{- end -}}