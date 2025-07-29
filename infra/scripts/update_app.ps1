# This code uploads the app source code at dockerhub

$IMAGE_NAME="jocosta96/soat-challenge:latest"
$APP_YAML="infra/deployment/dpm_app.yaml"
$WEBHOOK_YAML="infra/deployment/dpm_webhook.yaml"

Write-Output "atualizando imagem..."
docker build . -t "$IMAGE_NAME"
docker push "$IMAGE_NAME"


Write-Output "reiniciando pods..."
kubectl delete -f "$APP_YAML"
kubectl apply -f "$APP_YAML"
kubectl delete -f "$WEBHOOK_YAML"
kubectl apply -f "$WEBHOOK_YAML"

Write-Output "Atualizacao concluida"
Write-Output "URLs importantes:"
Write-Output "   Minikube IP: $(minikube ip)"
Write-Output "   API: http://$(minikube ip):30080"
Write-Output "   Swagger UI: http://$(minikube ip):30080/docs"
Write-Output "   Redoc UI: http://$(minikube ip):30080/redoc"
Write-Output ""