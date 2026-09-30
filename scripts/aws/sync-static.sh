#!/usr/bin/env bash
# Usage: scripts/aws/sync-static.sh <env> <tag> — publish the Vue 3 SPA build to S3 before the
# release, and invalidate CloudFront so the new index.html is served immediately (plan §7.1: no
# server to redeploy for the frontend, just a static bucket + CDN invalidation).
source "$(dirname "$0")/_common.sh"
require aws docker
load_env "${1:-}"
TAG="${2:?tag required}"

tmp="$(mktemp -d)"
cid="$(docker create "carepath-frontend:$TAG")"
trap 'docker rm -f "$cid" >/dev/null; rm -rf "$tmp"' EXIT
docker cp "$cid:/usr/share/nginx/html" "$tmp/dist"

# Hashed bundles (assets/*): cached for a year and never deleted (pages still open may request
# old ones). index.html itself must never be cached — it's what points at the new bundle hashes.
aws s3 sync "$tmp/dist/assets" "s3://$ASSETS_BUCKET/assets" --cache-control "public,max-age=31536000,immutable"
aws s3 sync "$tmp/dist" "s3://$ASSETS_BUCKET" --exclude "assets/*" --cache-control "no-cache"
aws cloudfront create-invalidation --distribution-id "$DISTRIBUTION_ID" --paths "/index.html" >/dev/null
log "static assets synced to s3://$ASSETS_BUCKET, CloudFront invalidated"
