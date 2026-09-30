#!/usr/bin/env bash
# Usage: scripts/aws/infra.sh <plan|apply|destroy> <staging|prod>   (Terraform or OpenTofu)
source "$(dirname "$0")/_common.sh"
action="${1:?action required: plan | apply | destroy}"
env="${2:?environment required: staging | prod}"
[[ "$env" =~ ^(staging|prod)$ ]] || die "env must be 'staging' or 'prod'"

tf="${TF:-$(command -v tofu || command -v terraform || true)}"
[[ -n "$tf" ]] || die "install tofu or terraform"
dir="$ROOT_DIR/infra/terraform/envs/$env"
[[ -f "$dir/backend.hcl" ]] || die "missing $dir/backend.hcl; run scripts/aws/bootstrap.sh first"

"$tf" -chdir="$dir" init -input=false -backend-config=backend.hcl
case "$action" in
  plan) "$tf" -chdir="$dir" plan -input=false -out=tfplan ;;
  apply) "$tf" -chdir="$dir" apply -input=false tfplan ;;
  destroy)
    read -rp "Type '$env' to destroy it: " confirm
    [[ "$confirm" == "$env" ]] || die "aborted"
    "$tf" -chdir="$dir" destroy -input=false
    ;;
  *) die "unknown action '$action'" ;;
esac
