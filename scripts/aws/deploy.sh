#!/usr/bin/env bash
# Usage: scripts/aws/deploy.sh <staging|prod> [tag]   (tag defaults to the current git SHA)
# build → push → register task defs → sync SPA → migrate → release (api, then worker, then beat)
# → wait → smoke test. api/worker/beat share one image (plan §15.3), so one build serves all three.
source "$(dirname "$0")/_common.sh"
require aws docker jq git curl
load_env "${1:-}"
TAG="${2:-$(git -C "$ROOT_DIR" rev-parse --short=12 HEAD)}"
if [[ -n "$(git -C "$ROOT_DIR" status --porcelain)" && -z "${ALLOW_DIRTY:-}" ]]; then
  die "working tree is dirty; commit first or set ALLOW_DIRTY=1"
fi

log "deploying $TAG to $ENV"
"$SCRIPT_DIR/build-push.sh" "$ENV" "$TAG"

api_def="$(register_task_def api api "$TAG")"
worker_def="$(register_task_def worker worker "$TAG")"
beat_def="$(register_task_def beat beat "$TAG")"
log "task definitions: $api_def, $worker_def, $beat_def"

"$SCRIPT_DIR/sync-static.sh" "$ENV" "$TAG"  # assets first: new HTML must find its bundles
"$SCRIPT_DIR/migrate.sh" "$ENV" "$api_def"  # stop here if the schema change fails

# api first (serves the new contract), then worker, then beat (the schedule-holding singleton).
aws ecs update-service --cluster "$CLUSTER" --service "$(family api)" --task-definition "$api_def" >/dev/null
aws ecs update-service --cluster "$CLUSTER" --service "$(family worker)" --task-definition "$worker_def" >/dev/null
aws ecs update-service --cluster "$CLUSTER" --service "$(family beat)" --task-definition "$beat_def" >/dev/null
log "waiting for services to become stable…"
aws ecs wait services-stable --cluster "$CLUSTER" --services "$(family api)" "$(family worker)" "$(family beat)"

"$SCRIPT_DIR/smoke-test.sh" "$ENV"
log "$TAG is live on https://$DOMAIN"
