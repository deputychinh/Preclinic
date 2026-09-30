variable "name" {
  type = string
}

variable "environment" {
  type = string
}

variable "alert_email" {
  type = string
}

variable "alb_arn_suffix" {
  type = string
}

variable "target_group_arn_suffixes" {
  description = "Service name → target group ARN suffix"
  type        = map(string)
}

variable "rds_identifier" {
  type = string
}

variable "redis_replication_group_id" {
  type = string
}

variable "monthly_budget_usd" {
  type = number
}
