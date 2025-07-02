#!/bin/bash
# This code uploads the app source code at dockerhub
set -e

IMAGE_NAME="jocosta96/soat-challenge:latest"

docker build . -t "$IMAGE_NAME"
docker push "$IMAGE_NAME"