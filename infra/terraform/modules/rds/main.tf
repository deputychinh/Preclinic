# PostgreSQL 16 in the private data subnets — chosen over the real-estate project's MySQL for
# JSONB and partial/expression indexes on RBAC-scoped queries (plan §2A.4). Encrypted with a
# customer-managed KMS key (not the AWS-managed default), automated backups; Multi-AZ and
# deletion protection switched on per environment.

resource "aws_db_subnet_group" "this" {
  name       = var.name
  subnet_ids = var.subnet_ids
}

resource "aws_db_parameter_group" "this" {
  name   = var.name
  family = "postgres16"

  parameter {
    name  = "rds.force_ssl"
    value = "1"
  }
}

resource "aws_db_instance" "this" {
  identifier                      = var.name
  engine                          = "postgres"
  engine_version                  = "16"
  instance_class                  = var.instance_class
  allocated_storage               = var.storage_gb
  max_allocated_storage           = var.storage_gb * 5
  storage_type                    = "gp3"
  storage_encrypted               = true
  kms_key_id                      = var.kms_key_id
  db_name                         = var.database
  username                        = var.username
  password                        = var.password
  db_subnet_group_name            = aws_db_subnet_group.this.name
  parameter_group_name            = aws_db_parameter_group.this.name
  vpc_security_group_ids          = [var.security_group_id]
  multi_az                        = var.multi_az
  publicly_accessible             = false
  backup_retention_period         = var.backup_days
  deletion_protection             = var.deletion_protection
  skip_final_snapshot             = !var.deletion_protection
  final_snapshot_identifier       = var.deletion_protection ? "${var.name}-final" : null
  auto_minor_version_upgrade      = true
  performance_insights_enabled    = true
  performance_insights_kms_key_id = var.kms_key_id
  copy_tags_to_snapshot           = true
}
