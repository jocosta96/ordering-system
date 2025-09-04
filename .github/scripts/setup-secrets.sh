#!/bin/bash

# Script to help setup GitHub secrets for deployment
# This script guides users through setting up required secrets

set -e

echo "🔐 GitHub Secrets Setup Guide"
echo "============================="
echo ""
echo "This script will help you set up the required GitHub secrets for automated deployment."
echo "You'll need to manually add these secrets to your GitHub repository settings."
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${BLUE}$1${NC}"
    echo "$(echo "$1" | sed 's/./-/g')"
}

print_instruction() {
    echo -e "${GREEN}$1${NC}"
}

print_warning() {
    echo -e "${YELLOW}$1${NC}"
}

print_header "1. Docker Hub Secrets"
echo ""
print_instruction "These secrets are required for building and pushing Docker images:"
echo ""
echo "Secret Name: DOCKER_USERNAME"
echo "Description: Your Docker Hub username"
echo "Value:       <your-dockerhub-username>"
echo ""
echo "Secret Name: DOCKER_PAT"
echo "Description: Docker Hub Personal Access Token (recommended)"
echo "Value:       <your-dockerhub-personal-access-token>"
echo ""
print_warning "💡 Tip: Use Docker Hub access tokens instead of passwords for better security"
print_warning "   Create at: https://hub.docker.com/settings/security"
echo ""

print_header "2. Kubernetes Configuration"
echo ""
print_instruction "This secret contains your Kubernetes cluster configuration:"
echo ""
echo "Secret Name: KUBE_CONFIG_DATA"
echo "Description: Base64 encoded kubeconfig file"
echo ""

# Check if kubeconfig exists
if [[ -f ~/.kube/config ]]; then
    print_instruction "✅ Found kubeconfig at ~/.kube/config"
    echo ""
    echo "To generate the secret value, run this command:"
    echo ""
    echo "    cat ~/.kube/config | base64 -w 0"
    echo ""
    print_warning "⚠️  Make sure this kubeconfig has the necessary permissions to deploy to your cluster"
else
    print_warning "⚠️  No kubeconfig found at ~/.kube/config"
    echo ""
    echo "Please ensure you have:"
    echo "1. A valid kubeconfig file"
    echo "2. Access to your Kubernetes cluster"
    echo "3. Proper permissions to deploy applications"
fi

echo ""

print_header "3. Application Secrets (Optional - if not already set)"
echo ""
print_instruction "These secrets may already exist from your existing workflows:"
echo ""

declare -a secrets=(
    "API_USER:Admin username for protected endpoints:admin"
    "API_PWD:Admin password for protected endpoints:admin123"
    "POSTGRES_DB:Database name:fastfood"
    "POSTGRES_HOST:Database host:localhost"
    "POSTGRES_PASSWORD:Database password:<your-database-password>"
    "POSTGRES_USER:Database username:postgres"
    "PGADMIN_MAIL:PgAdmin email:<your-email>"
    "PGADMIN_PW:PgAdmin password:<your-pgadmin-password>"
    "DRIVER_NAME:Database driver:postgresql"
)

for secret in "${secrets[@]}"; do
    IFS=':' read -r name description example <<< "$secret"
    echo "Secret Name: $name"
    echo "Description: $description"
    echo "Example:     $example"
    echo ""
done

print_header "4. GitHub Repository Setup"
echo ""
print_instruction "To add these secrets to your GitHub repository:"
echo ""
echo "1. Go to your repository on GitHub"
echo "2. Click on 'Settings' tab"
echo "3. Click on 'Secrets and variables' > 'Actions'"
echo "4. Click 'New repository secret'"
echo "5. Add each secret with the name and value shown above"
echo ""

print_header "5. Validation"
echo ""
print_instruction "After setting up secrets, you can:"
echo ""
echo "1. Push to main branch to trigger latest deployment"
echo "2. Create and push a tag to trigger tagged deployment"
echo "3. Check GitHub Actions tab for deployment status"
echo ""

print_header "6. Testing Your Setup"
echo ""
echo "To test your deployment setup:"
echo ""
echo "Option 1: Push to main branch"
echo "    git add ."
echo "    git commit -m 'feat: update deployment setup'"
echo "    git push origin main"
echo ""
echo "Option 2: Create a tag"
echo "    git tag v1.0.0"
echo "    git push origin v1.0.0"
echo ""

print_header "7. Troubleshooting"
echo ""
print_warning "Common issues and solutions:"
echo ""
echo "❌ Docker authentication failed"
echo "   Solution: Check DOCKER_USERNAME and DOCKER_PAT"
echo ""
echo "❌ Kubernetes access denied"
echo "   Solution: Verify KUBE_CONFIG_DATA and cluster permissions"
echo ""
echo "❌ Deployment timeouts"
echo "   Solution: Check cluster resources and pod startup times"
echo ""
echo "❌ Image pull failed"
echo "   Solution: Ensure image was pushed and is publicly accessible"
echo ""

print_header "8. Monitoring Your Deployment"
echo ""
echo "After deployment, you can monitor using:"
echo ""
echo "    kubectl get pods -l app=dpm-app"
echo "    kubectl logs -f deployment/dpm-app"
echo "    kubectl get hpa"
echo "    ./github/scripts/validate-deployment.sh"
echo ""

print_header "🚀 Ready to Deploy!"
echo ""
print_instruction "Once you've added all the secrets, your deployment pipeline will be ready."
print_instruction "Every push to main or new tag will trigger an automated deployment!"
echo ""
print_warning "💡 Remember to test in a development environment first!"

# Generate a checklist
echo ""
print_header "📋 Setup Checklist"
echo ""
echo "□ DOCKER_USERNAME secret added"
echo "□ DOCKER_PAT secret added"
echo "□ KUBE_CONFIG_DATA secret added"
echo "□ All application secrets verified (API_USER, API_PWD, etc.)"
echo "□ Kubernetes cluster is accessible"
echo "□ Docker Hub repository permissions verified"
echo "□ GitHub Actions enabled for repository"
echo "□ Test deployment performed"
echo ""
echo "✅ All items checked? You're ready to deploy!"
