# This code uploads the app source code at dockerhub

$IMAGE_NAME="jocosta96/soat-challenge:latest"
$APP_YAML="infra/deployment/dpm_app.yaml"

Write-Output "atualizando imagem..."
docker build . -t "$IMAGE_NAME"
docker push "$IMAGE_NAME"


Write-Output "reiniciando pods..."
kubectl delete -f "$APP_YAML"
kubectl apply -f "$APP_YAML"

Write-Output "Atualização concluída!"