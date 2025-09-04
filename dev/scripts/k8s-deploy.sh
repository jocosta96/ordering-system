#!/bin/bash

echo "Deploy do Sistema Kubernetes no Minikube"
echo "=================================="

echo "Iniciando Minikube..."
minikube start

echo "Aplicando manifests do Kubernetes..."

kubectl apply -f infra/deployment/

echo "Aguardando pods ficarem prontos..."
kubectl wait --for=condition=ready pod -l app=dpm-app --timeout=300s
kubectl wait --for=condition=ready pod -l app=dpm-database --timeout=300s

echo "Verificando status dos pods..."
kubectl get pods

echo ""
echo "Deploy concluído!"
echo ""
echo "URLs importantes:"
echo "   Minikube IP: $(minikube ip)"
echo "   API: http://$(minikube ip):30080"
echo "   Swagger UI: http://$(minikube ip):30080/docs"
echo "   Redoc UI: http://$(minikube ip):30080/redoc"
echo ""
echo "Para ver logs:"
echo "   kubectl logs -f deployment/dpm-app"
echo ""
echo "Para verificar HPA:"
echo "   kubectl get hpa" 