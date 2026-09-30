#!/usr/bin/env bash
# Usage: scripts/aws/smoke-test.sh <env> — the public site and API answer through CloudFront.
source "$(dirname "$0")/_common.sh"
require curl
load_env "${1:-}"

check() {
  local url="$1" attempt
  for attempt in 1 2 3 4 5; do
    if curl -fsS -o /dev/null --max-time 10 "$url"; then
      log "OK  $url"
      return 0
    fi
    log "retry $attempt: $url"
    sleep $((attempt * 3))
  done
  die "smoke test failed: $url"
}

check "https://$DOMAIN/api/v1/health"
check "https://$DOMAIN/"
check "https://$DOMAIN/login"
