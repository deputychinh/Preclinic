#!/usr/bin/env bash
# Usage: scripts/aws/seed.sh <env> — load demo data (care team, patients, signed encounter, one
# pending AI draft) with the running API image.
source "$(dirname "$0")/_common.sh"
require aws jq
load_env "${1:-}"
[[ "$ENV" == "prod" ]] && die "demo data is for staging only"
task_def="$(aws ecs describe-services --cluster "$CLUSTER" --services "$(family api)" \
  --query 'services[0].taskDefinition' --output text)"
run_api_task "$task_def" python manage.py seed_demo
log "demo data loaded"
