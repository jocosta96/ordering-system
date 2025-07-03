#!/bin/bash
# This code uploads the app source code at dockerhub
set -e

IMAGE_NAME="jocosta96/soat-challenge:latest"
APP_YAML="infra/deployment/dpm_app.yaml"

docker build . -t "$IMAGE_NAME"
docker push "$IMAGE_NAME"

kubectl delete -f "$APP_YAML"
kubectl apply -f "$APP_YAML"