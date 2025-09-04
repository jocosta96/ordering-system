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

print_header "2. Application Secrets (Optional - if not already set)"
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

print_header "3. GitHub Repository Setup"
echo ""
print_instruction "To add these secrets to your GitHub repository:"
echo ""
echo "1. Go to your repository on GitHub"
echo "2. Click on 'Settings' tab"
echo "3. Click on 'Secrets and variables' > 'Actions'"
echo "4. Click 'New repository secret'"
echo "5. Add each secret with the name and value shown above"
echo ""

print_header "4. Validation"
echo ""
print_instruction "After setting up secrets, you can:"
echo ""
echo "1. Push to main branch to trigger latest image build"
echo "2. Use manual workflow dispatch to trigger custom tagged build"
echo "3. Check GitHub Actions tab for build status"
echo "4. Verify images on Docker Hub"
echo ""

print_header "5. Testing Your Setup"
echo ""
echo "To test your build setup:"
echo ""
echo "Option 1: Push to main branch"
echo "    git add ."
echo "    git commit -m 'feat: setup automated image build'"
echo "    git push origin main"
echo ""
echo "Option 2: Manual workflow dispatch"
echo "    1. Go to GitHub Actions tab"
echo "    2. Click 'Build and Push Docker Image' workflow"
echo "    3. Click 'Run workflow'"
echo "    4. Enter tag (e.g., v1.0.0)"
echo "    5. Click 'Run workflow'"
echo ""

print_header "6. Troubleshooting"
echo ""
print_warning "Common issues and solutions:"
echo ""
echo "❌ Docker authentication failed"
echo "   Solution: Check DOCKER_USERNAME and DOCKER_PAT"
echo ""
echo "❌ Build failed"
echo "   Solution: Check Dockerfile syntax and dependencies"
echo ""
echo "❌ Multi-platform build issues"
echo "   Solution: Verify base images support target architectures"
echo ""
echo "❌ Image not found on Docker Hub"
echo "   Solution: Check GitHub Actions logs for push errors"
echo ""

print_header "7. Monitoring Your Build"
echo ""
echo "After build completion, you can monitor using:"
echo ""
echo "    # Check GitHub Actions status"
echo "    # https://github.com/your-repo/actions"
echo "    "
echo "    # Verify images on Docker Hub"
echo "    # https://hub.docker.com/r/jocosta96/soat-challenge"
echo "    "
echo "    # Pull and test images locally"
echo "    docker pull jocosta96/soat-challenge:latest"
echo "    docker pull jocosta96/soat-challenge:v1.0.0"
echo ""

print_header "🚀 Ready to Build!"
echo ""
print_instruction "Once you've added all the secrets, your build pipeline will be ready."
print_instruction "Every push to main or new tag will trigger an automated image build!"
echo ""
print_instruction "🏗️ For deployment: Use the built images in your infrastructure repository."
print_warning "💡 Remember to test builds in a development environment first!"

# Generate a checklist
echo ""
print_header "📋 Setup Checklist"
echo ""
echo "□ DOCKER_USERNAME secret added"
echo "□ DOCKER_PAT secret added"
echo "□ All application secrets verified (API_USER, API_PWD, etc.)"
echo "□ Docker Hub repository permissions verified"
echo "□ GitHub Actions enabled for repository"
echo "□ Test build performed"
echo "□ Infrastructure repository ready for image deployment"
echo ""
echo "✅ All items checked? You're ready to build!"
