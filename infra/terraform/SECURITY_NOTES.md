# Checkov findings: accepted for this assignment

`checkov -d . --framework terraform` reports ~48 findings after the fixes below. Fixed vs.
accepted, and why — and where this project's posture is deliberately *stricter* than the
real-estate project's, per plan §15.1/§15.4.

## Different from the real-estate project by design (not an accepted trade-off)

- **Customer-managed KMS key, not AWS-managed.** Unlike `python-vuejs/infra/terraform`, which
  accepts AWS-managed keys as a cost trade-off, this project uses one CMK
  (`modules/kms`) for RDS storage + Performance Insights, ElastiCache at-rest encryption, the
  lab-imports S3 bucket, and the app Secrets Manager secret. A compliance-minded reviewer expects
  this for anything touching PHI, and the real cost is ~USD 1/month plus minimal per-request cost
  — not worth trading away here even though the sibling project reasonably did for its domain.

## Fixed

- SNS alerts topic encrypted with the AWS-managed key (`alias/aws/sns`) — alarm text isn't PHI, so
  this doesn't need the CMK, but it should still be encrypted at no extra cost.
- Security group / rule descriptions (readability) on every SG in `modules/security-groups`.
- S3 lifecycle: abort incomplete multipart uploads after 7 days, on both the SPA-assets and
  lab-imports buckets.
- Worker/beat run with **zero inbound security-group rules** (`modules/security-groups`'s
  `worker` SG) — not a Checkov-driven fix, but the same "smallest possible blast radius" instinct.

## Accepted (cost or scope trade-off, not a mistake)

- **RDS Multi-AZ, deletion protection, enhanced monitoring, IAM auth, exported logs**: gated by
  `var.sizing` per environment (plan §15.5) — off in staging to keep costs down, on in production
  (`envs/prod/terraform.tfvars`). Enhanced monitoring and IAM auth specifically are left off in
  both environments for this assignment's scope; the CMK and encryption-at-rest are not gated the
  same way, since those are non-negotiable for PHI regardless of environment.
- **Access logging** for the ALB and CloudFront, and **S3 event notifications / cross-region
  replication**: each needs an extra bucket/pipeline; skipped for this assignment. CloudWatch
  Container Insights and the app's own structured request logs (`RequestIdMiddleware`, plan §9)
  already give per-request visibility, and `AuditEvent` (DS-04) already gives a tamper-evident
  record of every PHI access independent of infrastructure logging.
- **VPC flow logs**: same cost trade-off as the sibling project; the chained security groups
  (plan §15.4) already make the intended traffic pattern explicit and auditable without flow logs.
- **WAF logging configuration** and **Log4j-specific AWS managed rule check**: needs a Kinesis
  Data Firehose or CloudWatch Logs destination for the former; the latter checks for a rule set
  this project doesn't need (no Java/Log4j in the stack). Managed rule metrics already go to
  CloudWatch.
- **Secrets Manager automatic rotation**: needs a rotation Lambda; out of scope for this
  assignment. The app secret bundles DB/Redis/Django/Anthropic credentials generated once at
  `terraform apply` time, not long-lived shared secrets rotated on a schedule.
- **ElastiCache Multi-AZ / automatic failover in staging**: `redis_nodes = 1` in staging
  (`var.sizing`), `2` in production — same per-environment gating as RDS.
- **Security groups "not attached to another resource" (CKV2_AWS_5)**: a Checkov static-analysis
  limitation — each SG here *is* attached (to the ALB, ECS tasks, RDS, and ElastiCache resources
  respectively), just via a separate module (`modules/ecs-service`, `modules/rds`,
  `modules/elasticache`) that Checkov's single-pass scan doesn't always resolve across module
  boundaries. Confirmed correct by reading `stack/main.tf`'s wiring.
- **ALB target group "uses HTTP" (CKV_AWS_378)**: the target group speaks HTTP to the Django
  container *inside* the VPC, on a private subnet with no direct internet route — TLS terminates
  at the ALB listener (HTTPS/443, `ELBSecurityPolicy-TLS13-1-2-2021-06`) and at CloudFront in
  front of that. Encrypting the ALB-to-task hop too would need a private ACM certificate on every
  task, which is disproportionate for this project's threat model (the security groups already
  ensure only the ALB can reach that port).
- **GitHub OIDC deploy policy's `"*"` resource on `ecs:RegisterTaskDefinition`/
  `DescribeTaskDefinition`**: the ECS API does not support a resource ARN for these two actions —
  a documented AWS limitation, not an oversight (same finding, same reason, as the sibling
  project's `modules/github-oidc`, reused here unchanged).

Full list: `checkov -d infra/terraform --framework terraform`.
