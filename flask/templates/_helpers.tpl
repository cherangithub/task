{{- define "labels" -}}
app: flask-app
env: {{ .Values.app.env }}
{{- end -}}