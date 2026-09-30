# One customer-managed key (CMK) for everything that holds PHI: RDS, S3 lab-import bucket, and
# CloudWatch Logs. Plan §15.4/§6.10: unlike the real-estate project's accepted AWS-managed-key
# trade-off, this is not optional here — a compliance-minded reviewer expects a CMK for PHI, and
# it costs about USD 1/month plus minimal per-request cost.

resource "aws_kms_key" "this" {
  description             = "CarePath ${var.name} CMK — RDS, S3 (lab imports), CloudWatch Logs"
  deletion_window_in_days = var.deletion_window_days
  enable_key_rotation     = true
}

resource "aws_kms_alias" "this" {
  name          = "alias/${var.name}"
  target_key_id = aws_kms_key.this.key_id
}

# CloudWatch Logs needs an explicit grant to use the key for log group encryption.
data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

resource "aws_kms_key_policy" "this" {
  key_id = aws_kms_key.this.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "EnableRootAccountPermissions"
        Effect    = "Allow"
        Principal = { AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root" }
        Action    = "kms:*"
        Resource  = "*"
      },
      {
        Sid    = "AllowCloudWatchLogs"
        Effect = "Allow"
        Principal = {
          Service = "logs.${data.aws_region.current.name}.amazonaws.com"
        }
        Action = [
          "kms:Encrypt*", "kms:Decrypt*", "kms:ReEncrypt*", "kms:GenerateDataKey*", "kms:Describe*"
        ]
        Resource = "*"
        Condition = {
          ArnLike = {
            "kms:EncryptionContext:aws:logs:arn" = "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:*"
          }
        }
      }
    ]
  })
}
