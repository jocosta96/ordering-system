#!/bin/bash

# Deployment validation script
# This script validates that the deployment was successful

set -e

echo "🔍 Validating Fast Food Ordering System Deployment"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    local status=$1
    local message=$2
    
    if [[ "$status" == "SUCCESS" ]]; then
        echo -e "${GREEN}✅ $message${NC}"
    elif [[ "$status" == "WARNING" ]]; then
        echo -e "${YELLOW}⚠️  $message${NC}"
    elif [[ "$status" == "ERROR" ]]; then
        echo -e "${RED}❌ $message${NC}"
    else
        echo -e "$message"
    fi
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo ""
echo "🔧 Checking Prerequisites"
echo "========================"

if command_exists kubectl; then
    print_status "SUCCESS" "kubectl is installed"
else
    print_status "ERROR" "kubectl is not installed"
    exit 1
fi

if command_exists curl; then
    print_status "SUCCESS" "curl is available"
else
    print_status "WARNING" "curl is not available - skipping endpoint tests"
fi

# Check cluster connectivity
echo ""
echo "☸️  Checking Kubernetes Cluster"
echo "==============================="

if kubectl cluster-info >/dev/null 2>&1; then
    print_status "SUCCESS" "Connected to Kubernetes cluster"
    echo "   Cluster: $(kubectl config current-context)"
else
    print_status "ERROR" "Cannot connect to Kubernetes cluster"
    echo "   Please check your kubeconfig and cluster connectivity"
    exit 1
fi

# Check namespace
NAMESPACE=$(kubectl config view --minify --output 'jsonpath={..namespace}')
if [[ -z "$NAMESPACE" ]]; then
    NAMESPACE="default"
fi
print_status "INFO" "Using namespace: $NAMESPACE"

# Check deployments
echo ""
echo "🚀 Checking Deployments"
echo "======================"

# Check main application
if kubectl get deployment dpm-app >/dev/null 2>&1; then
    APP_READY=$(kubectl get deployment dpm-app -o jsonpath='{.status.readyReplicas}')
    APP_DESIRED=$(kubectl get deployment dpm-app -o jsonpath='{.spec.replicas}')
    
    if [[ "$APP_READY" == "$APP_DESIRED" ]]; then
        print_status "SUCCESS" "Application deployment is ready ($APP_READY/$APP_DESIRED replicas)"
    else
        print_status "WARNING" "Application deployment is not fully ready ($APP_READY/$APP_DESIRED replicas)"
    fi
else
    print_status "ERROR" "Application deployment not found"
fi

# Check webhook
if kubectl get deployment dpm-webhook >/dev/null 2>&1; then
    WEBHOOK_READY=$(kubectl get deployment dpm-webhook -o jsonpath='{.status.readyReplicas}')
    WEBHOOK_DESIRED=$(kubectl get deployment dpm-webhook -o jsonpath='{.spec.replicas}')
    
    if [[ "$WEBHOOK_READY" == "$WEBHOOK_DESIRED" ]]; then
        print_status "SUCCESS" "Webhook deployment is ready ($WEBHOOK_READY/$WEBHOOK_DESIRED replicas)"
    else
        print_status "WARNING" "Webhook deployment is not fully ready ($WEBHOOK_READY/$WEBHOOK_DESIRED replicas)"
    fi
else
    print_status "WARNING" "Webhook deployment not found"
fi

# Check database
if kubectl get deployment dmp-database >/dev/null 2>&1; then
    DB_READY=$(kubectl get deployment dmp-database -o jsonpath='{.status.readyReplicas}')
    DB_DESIRED=$(kubectl get deployment dmp-database -o jsonpath='{.spec.replicas}')
    
    if [[ "$DB_READY" == "$DB_DESIRED" ]]; then
        print_status "SUCCESS" "Database deployment is ready ($DB_READY/$DB_DESIRED replicas)"
    else
        print_status "WARNING" "Database deployment is not fully ready ($DB_READY/$DB_DESIRED replicas)"
    fi
else
    print_status "WARNING" "Database deployment not found"
fi

# Check services
echo ""
echo "🌐 Checking Services"
echo "==================="

# Check application service
if kubectl get service svc-app-nodeport >/dev/null 2>&1; then
    print_status "SUCCESS" "Application service exists"
    APP_PORT=$(kubectl get service svc-app-nodeport -o jsonpath='{.spec.ports[0].nodePort}')
    print_status "INFO" "Application NodePort: $APP_PORT"
else
    print_status "WARNING" "Application service not found"
fi

# Check webhook service
if kubectl get service svc-webhook-nodeport >/dev/null 2>&1; then
    print_status "SUCCESS" "Webhook service exists"
    WEBHOOK_PORT=$(kubectl get service svc-webhook-nodeport -o jsonpath='{.spec.ports[0].nodePort}')
    print_status "INFO" "Webhook NodePort: $WEBHOOK_PORT"
else
    print_status "WARNING" "Webhook service not found"
fi

# Check HPA
echo ""
echo "📈 Checking Auto-scaling"
echo "======================="

if kubectl get hpa hpa-app >/dev/null 2>&1; then
    HPA_MIN=$(kubectl get hpa hpa-app -o jsonpath='{.spec.minReplicas}')
    HPA_MAX=$(kubectl get hpa hpa-app -o jsonpath='{.spec.maxReplicas}')
    HPA_CPU=$(kubectl get hpa hpa-app -o jsonpath='{.spec.targetCPUUtilizationPercentage}')
    
    print_status "SUCCESS" "HPA is configured"
    print_status "INFO" "Scale: $HPA_MIN-$HPA_MAX replicas, CPU threshold: $HPA_CPU%"
else
    print_status "WARNING" "HPA not found - auto-scaling not configured"
fi

# Check pods
echo ""
echo "🐳 Checking Pod Status"
echo "====================="

# Application pods
APP_PODS=$(kubectl get pods -l app=dpm-app --no-headers 2>/dev/null | wc -l)
if [[ "$APP_PODS" -gt 0 ]]; then
    print_status "SUCCESS" "Found $APP_PODS application pod(s)"
    
    # Check pod status
    RUNNING_PODS=$(kubectl get pods -l app=dpm-app --field-selector=status.phase=Running --no-headers 2>/dev/null | wc -l)
    if [[ "$RUNNING_PODS" == "$APP_PODS" ]]; then
        print_status "SUCCESS" "All application pods are running"
    else
        print_status "WARNING" "Only $RUNNING_PODS/$APP_PODS application pods are running"
    fi
else
    print_status "ERROR" "No application pods found"
fi

# Webhook pods
WEBHOOK_PODS=$(kubectl get pods -l app=dpm-webhook --no-headers 2>/dev/null | wc -l)
if [[ "$WEBHOOK_PODS" -gt 0 ]]; then
    print_status "SUCCESS" "Found $WEBHOOK_PODS webhook pod(s)"
else
    print_status "WARNING" "No webhook pods found"
fi

# Check secrets and configmaps
echo ""
echo "🔐 Checking Configuration"
echo "========================"

# Check secrets
if kubectl get secret sec-app >/dev/null 2>&1; then
    print_status "SUCCESS" "Application secrets exist"
else
    print_status "ERROR" "Application secrets not found"
fi

if kubectl get secret sec-database >/dev/null 2>&1; then
    print_status "SUCCESS" "Database secrets exist"
else
    print_status "ERROR" "Database secrets not found"
fi

# Check configmaps
if kubectl get configmap cfm-database >/dev/null 2>&1; then
    print_status "SUCCESS" "Database config exists"
else
    print_status "WARNING" "Database config not found"
fi

# Test endpoints if possible
echo ""
echo "🏥 Testing Health Endpoints"
echo "=========================="

if command_exists curl && [[ -n "$APP_PORT" ]]; then
    # Try to get cluster IP or use port-forward
    if command_exists minikube && minikube status >/dev/null 2>&1; then
        CLUSTER_IP=$(minikube ip 2>/dev/null)
        if [[ -n "$CLUSTER_IP" ]]; then
            print_status "INFO" "Testing endpoints on Minikube: $CLUSTER_IP:$APP_PORT"
            
            if curl -s --connect-timeout 5 "http://$CLUSTER_IP:$APP_PORT/health" >/dev/null 2>&1; then
                print_status "SUCCESS" "Health endpoint is responding"
            else
                print_status "WARNING" "Health endpoint is not responding"
            fi
            
            if curl -s --connect-timeout 5 "http://$CLUSTER_IP:$APP_PORT/docs" >/dev/null 2>&1; then
                print_status "SUCCESS" "API documentation is accessible"
            else
                print_status "WARNING" "API documentation is not accessible"
            fi
        fi
    else
        print_status "INFO" "Cluster IP not accessible - skipping endpoint tests"
        print_status "INFO" "To test manually: kubectl port-forward service/svc-app-nodeport 8080:80"
        print_status "INFO" "Then visit: http://localhost:8080/health"
    fi
else
    print_status "INFO" "Skipping endpoint tests (curl not available or service not found)"
fi

# Summary
echo ""
echo "📊 Deployment Summary"
echo "===================="

# Count successful checks
TOTAL_CHECKS=0
SUCCESSFUL_CHECKS=0

# This is a simplified summary - in a real script you'd track these
print_status "INFO" "Deployment validation completed"
print_status "INFO" "Check the results above for any issues that need attention"

echo ""
echo "🔗 Useful Commands"
echo "=================="
echo "View application logs:     kubectl logs -f deployment/dpm-app"
echo "View webhook logs:         kubectl logs -f deployment/dpm-webhook"
echo "Check pod status:          kubectl get pods -l app=dpm-app"
echo "Check HPA status:          kubectl get hpa"
echo "Port-forward for testing:  kubectl port-forward service/svc-app-nodeport 8080:80"

echo ""
echo "✅ Validation completed! Check any warnings or errors above."
