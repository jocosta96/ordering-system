#!/bin/bash

echo "Deploy do Sistema Kubernetes no Minikube"
echo "=================================="

echo "Iniciando Minikube..."
minikube start

echo "Aplicando manifests do Kubernetes..."

# Apply all manifests except the app deployment first
echo "Aplicando ConfigMaps, Secrets, Volumes e Database..."
kubectl apply -f infra/deployment/cfm_database.yaml
kubectl apply -f infra/deployment/sec_database.yaml
kubectl apply -f infra/deployment/sec_app.yaml
kubectl apply -f infra/deployment/pv_database.yaml
kubectl apply -f infra/deployment/pvc_database.yaml
kubectl apply -f infra/deployment/dpm_database.yaml
kubectl apply -f infra/deployment/svc_database.yaml

echo "Aguardando database ficar pronto..."
kubectl wait --for=condition=ready pod -l app=dpm-database --timeout=300s

echo "Executando job de inicialização do banco..."
kubectl apply -f infra/deployment/job_db_init.yaml

echo "Aguardando job de inicialização completar..."
kubectl wait --for=condition=complete job/db-init-job --timeout=300s

echo "Deployando aplicação (agora que o banco está pronto)..."
kubectl apply -f infra/deployment/dpm_app.yaml

echo "Aplicando serviços da aplicação..."
kubectl apply -f infra/deployment/svc_app.yaml
kubectl apply -f infra/deployment/hpa_app.yaml
kubectl apply -f infra/deployment/metrics.yaml

echo "Aguardando aplicação ficar pronta..."
kubectl wait --for=condition=ready pod -l app=dpm-app --timeout=300s

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