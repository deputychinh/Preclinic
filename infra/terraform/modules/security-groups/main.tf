# Security groups chained by reference, never by CIDR (plan §15.4):
# CloudFront → ALB → API → RDS/Redis. The worker/beat tasks have zero inbound rules — they only
# make outbound calls (DB, Redis, S3, Claude API), so nothing in the VPC can reach them directly.

data "aws_ec2_managed_prefix_list" "cloudfront" {
  name = "com.amazonaws.global.cloudfront.origin-facing"
}

resource "aws_security_group" "alb" {
  name        = "${var.name}-alb"
  description = "HTTPS from CloudFront only"
  vpc_id      = var.vpc_id
}

resource "aws_vpc_security_group_ingress_rule" "alb_https" {
  security_group_id = aws_security_group.alb.id
  description       = "HTTPS from CloudFront"
  prefix_list_id    = data.aws_ec2_managed_prefix_list.cloudfront.id
  ip_protocol       = "tcp"
  from_port         = 443
  to_port           = 443
}

resource "aws_security_group" "api" {
  name        = "${var.name}-api"
  description = "Django/DRF tasks"
  vpc_id      = var.vpc_id
}

resource "aws_vpc_security_group_ingress_rule" "api_from_alb" {
  security_group_id            = aws_security_group.api.id
  description                  = "Django from the ALB"
  referenced_security_group_id = aws_security_group.alb.id
  ip_protocol                  = "tcp"
  from_port                    = 8000
  to_port                      = 8000
}

# Worker/beat: no ingress rule at all (§15.4) — they only enqueue/dequeue via Redis and call out
# to Postgres, S3 and the Claude API. Kept as its own SG so this "no inbound" fact is explicit and
# auditable, not just an absence of rules on a shared SG.
resource "aws_security_group" "worker" {
  name        = "${var.name}-worker"
  description = "Celery worker/beat — outbound only, zero inbound rules"
  vpc_id      = var.vpc_id
}

resource "aws_security_group" "rds" {
  name        = "${var.name}-rds"
  description = "PostgreSQL from the API and worker only"
  vpc_id      = var.vpc_id
}

resource "aws_vpc_security_group_ingress_rule" "rds_from_api" {
  security_group_id            = aws_security_group.rds.id
  description                  = "PostgreSQL from the API"
  referenced_security_group_id = aws_security_group.api.id
  ip_protocol                  = "tcp"
  from_port                    = 5432
  to_port                      = 5432
}

resource "aws_vpc_security_group_ingress_rule" "rds_from_worker" {
  security_group_id            = aws_security_group.rds.id
  description                  = "PostgreSQL from the worker/beat"
  referenced_security_group_id = aws_security_group.worker.id
  ip_protocol                  = "tcp"
  from_port                    = 5432
  to_port                      = 5432
}

resource "aws_security_group" "redis" {
  name        = "${var.name}-redis"
  description = "Redis from the API and worker only"
  vpc_id      = var.vpc_id
}

resource "aws_vpc_security_group_ingress_rule" "redis_from_api" {
  security_group_id            = aws_security_group.redis.id
  description                  = "Redis from the API"
  referenced_security_group_id = aws_security_group.api.id
  ip_protocol                  = "tcp"
  from_port                    = 6379
  to_port                      = 6379
}

resource "aws_vpc_security_group_ingress_rule" "redis_from_worker" {
  security_group_id            = aws_security_group.redis.id
  description                  = "Redis from the worker/beat"
  referenced_security_group_id = aws_security_group.worker.id
  ip_protocol                  = "tcp"
  from_port                    = 6379
  to_port                      = 6379
}

# Outbound: ALB to tasks; API and worker to anywhere (ECR, S3, Claude API, CloudWatch through NAT).
resource "aws_vpc_security_group_egress_rule" "all" {
  for_each = {
    alb    = aws_security_group.alb.id
    api    = aws_security_group.api.id
    worker = aws_security_group.worker.id
  }
  security_group_id = each.value
  description       = "Outbound: ECR, S3, Claude API, CloudWatch, upstream services"
  ip_protocol       = "-1"
  cidr_ipv4         = "0.0.0.0/0"
}
