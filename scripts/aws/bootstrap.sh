#!/usr/bin/env bash
# Usage: scripts/aws/bootstrap.sh — once per AWS account: Terraform state bucket + backend.hcl files.
source "$(dirname "$0")/_common.sh"
require aws

account="$(aws sts get-caller-identity --query Account --output text)"
bucket="${PROJECT}-tfstate-${account}"

if aws s3api head-bucket --bucket "$bucket" 2>/dev/null; then
  log "state bucket $bucket already exists"
else
  aws s3api create-bucket --bucket "$bucket" --create-bucket-configuration LocationConstraint="$AWS_REGION" >/dev/null
  log "created $bucket"
fi
aws s3api put-bucket-versioning --bucket "$bucket" --versioning-configuration Status=Enabled
aws s3api put-bucket-encryption --bucket "$bucket" \
  --server-side-encryption-configuration '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}'
aws s3api put-public-access-block --bucket "$bucket" --public-access-block-configuration \
  BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true

for env in staging prod; do
  sed "s/ACCOUNT_ID/${account}/" "$ROOT_DIR/infra/terraform/envs/$env/backend.hcl.example" \
    >"$ROOT_DIR/infra/terraform/envs/$env/backend.hcl"
done
log "wrote infra/terraform/envs/{staging,prod}/backend.hcl"
