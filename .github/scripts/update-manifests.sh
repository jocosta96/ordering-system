#!/bin/bash

# Script to update Kubernetes manifests with new Docker image tag
# Usage: ./update-manifests.sh <image-tag>

set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <image-tag>"
    echo "Example: $0 latest"
    echo "Example: $0 v1.2.3"
    exit 1
fi

IMAGE_TAG="$1"
IMAGE_NAME="jocosta96/soat-challenge"
FULL_IMAGE="${IMAGE_NAME}:${IMAGE_TAG}"

echo "Updating Kubernetes manifests with image: ${FULL_IMAGE}"

# Backup original files
cp dev/k8s/dpm_app.yaml dev/k8s/dpm_app.yaml.bak
cp dev/k8s/dpm_webhook.yaml dev/k8s/dpm_webhook.yaml.bak

# Update main application deployment
sed -i.tmp "s|image: ${IMAGE_NAME}:.*|image: ${FULL_IMAGE}|g" dev/k8s/dpm_app.yaml
rm -f dev/k8s/dpm_app.yaml.tmp

# Update webhook deployment  
sed -i.tmp "s|image: ${IMAGE_NAME}:.*|image: ${FULL_IMAGE}|g" dev/k8s/dpm_webhook.yaml
rm -f dev/k8s/dmp_webhook.yaml.tmp

echo "✅ Successfully updated manifests with image: ${FULL_IMAGE}"

# Verify changes
echo "📋 Updated files:"
echo "  - dev/k8s/dpm_app.yaml"
echo "  - dev/k8s/dpm_webhook.yaml"

echo ""
echo "📝 Changes made:"
grep "image: ${IMAGE_NAME}" dev/k8s/dpm_app.yaml || echo "  App image updated"
grep "image: ${IMAGE_NAME}" dev/k8s/dpm_webhook.yaml || echo "  Webhook image updated"
