#!/bin/bash
# This code uploads the app source code at dockerhub
set -e

IMAGE_NAME="jocosta96/soat-challenge:dev"
APP_YAML="infra/deployment/dpm_app.yaml"
WEBHOOK_YAML="infra/deployment/dpm_webhook.yaml"

echo "atualizando imagem..."
docker build . -t "$IMAGE_NAME"
docker push "$IMAGE_NAME"


echo "reiniciando pods..."
kubectl delete -f "$APP_YAML"
kubectl apply -f "$APP_YAML"
kubectl delete -f "$WEBHOOK_YAML"
kubectl apply -f "$WEBHOOK_YAML"

echo "Atualização concluída!"
echo "URLs importantes:"
echo "   Minikube IP: $(minikube ip)"
echo "   API: http://$(minikube ip):30080"
echo "   Swagger UI: http://$(minikube ip):30080/docs"
echo "   Redoc UI: http://$(minikube ip):30080/redoc"
echo ""