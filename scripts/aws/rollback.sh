#!/usr/bin/env bash
# Usage: scripts/aws/rollback.sh <env> [service] — move services back one task-definition revision.
# Database migrations are not reverted: expand/contract keeps the previous code compatible.
source "$(dirname "$0")/_common.sh"
require aws
load_env "${1:-}"
if [[ -n "${2:-}" ]]; then targets=("$2"); else targets=("${ECS_SERVICES[@]}"); fi

names=()
for svc in "${targets[@]}"; do
  current="$(aws ecs describe-services --cluster "$CLUSTER" --services "$(family "$svc")" \
    --query 'services[0].taskDefinition' --output text)"
  previous="${current%:*}:$((${current##*:} - 1))"
  log "$svc: $current → $previous"
  aws ecs update-service --cluster "$CLUSTER" --service "$(family "$svc")" --task-definition "$previous" >/dev/null
  names+=("$(family "$svc")")
done
aws ecs wait services-stable --cluster "$CLUSTER" --services "${names[@]}"
"$SCRIPT_DIR/smoke-test.sh" "$ENV"
