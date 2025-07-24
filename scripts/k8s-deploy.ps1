Write-Output "Deploy do Sistema Kubernetes no Minikube"
Write-Output "=================================="

Write-Output "Iniciando Minikube..."
minikube start

Write-Output "Aplicando manifests do Kubernetes..."

kubectl apply -f infra/deployment/

Write-Output "Aguardando pods ficarem prontos..."
kubectl wait --for=condition=ready pod -l app=dpm-app --timeout=300s
kubectl wait --for=condition=ready pod -l app=dpm-database --timeout=300s

Write-Output "Verificando status dos pods..."
kubectl get pods

Write-Output ""
Write-Output "Deploy concluído!"
Write-Output ""
Write-Output "URLs importantes:"
Write-Output "   Minikube IP: $(minikube ip)"
Write-Output "   API: http://$(minikube ip):30080"
Write-Output "   Swagger UI: http://$(minikube ip):30080/docs"
Write-Output "   Redoc UI: http://$(minikube ip):30080/redoc"
Write-Output ""
Write-Output "Para ver logs:"
Write-Output "   kubectl logs -f deployment/dpm-app"
Write-Output ""
Write-Output "Para verificar HPA:"
Write-Output "   kubectl get hpa" 