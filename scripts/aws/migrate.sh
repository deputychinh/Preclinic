#!/usr/bin/env bash
# Usage: scripts/aws/migrate.sh <env> <api-task-def-arn>
# Runs Django migrations with the NEW image before traffic moves. Migrations must stay backward
# compatible (expand/contract), because the old code keeps serving until the release finishes.
source "$(dirname "$0")/_common.sh"
require aws jq
load_env "${1:-}"
run_api_task "${2:?task definition ARN required}" python manage.py migrate --noinput
log "migrations applied"
