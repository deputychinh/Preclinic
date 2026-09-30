#!/usr/bin/env bash
# Usage: scripts/aws/build-push.sh <env> <tag> — build the backend image (shared by api/worker/beat)
# for linux/amd64 and push to ECR, and build the frontend SPA (published by sync-static.sh instead).
source "$(dirname "$0")/_common.sh"
require aws docker
load_env "${1:-}"
TAG="${2:?tag required}"

aws ecr get-login-password | docker login --username AWS --password-stdin "$ECR_REGISTRY"
log "build backend:$TAG"
docker buildx build --platform linux/amd64 --push -t "$(image_uri "$TAG")" "$ROOT_DIR/backend"

log "build frontend:$TAG (for sync-static.sh — not pushed to ECR, it's a static SPA, plan §7.1)"
docker build --build-arg "VITE_API_BASE_URL=https://${DOMAIN}/api/v1" -t "carepath-frontend:$TAG" "$ROOT_DIR/frontend"
