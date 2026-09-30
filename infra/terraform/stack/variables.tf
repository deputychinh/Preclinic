variable "project" {
  type    = string
  default = "carepath"
}

variable "environment" {
  description = "staging | prod"
  type        = string
  validation {
    condition     = contains(["staging", "prod"], var.environment)
    error_message = "environment must be staging or prod."
  }
}

variable "azs" {
  type = list(string)
}

variable "vpc_cidr" {
  type = string
}

variable "zone_name" {
  description = "Existing Route 53 hosted zone"
  type        = string
}

variable "domain" {
  description = "Public site domain, e.g. staging.example.com"
  type        = string
}

variable "github_repository" {
  description = "owner/name, allowed to deploy through OIDC"
  type        = string
}

variable "create_github_oidc_provider" {
  type    = bool
  default = true
}

variable "alert_email" {
  type = string
}

variable "monthly_budget_usd" {
  type = number
}

variable "anthropic_api_key" {
  description = "Claude API key for the AI clinical assistant (plan §6.9) — set outside version control"
  type        = string
  sensitive   = true
}

variable "initial_image_tag" {
  description = "Image tag for the first task definition; later releases come from scripts/aws/deploy.sh"
  type        = string
  default     = "bootstrap"
}

variable "sizing" {
  description = "Per-environment capacity (plan §15.5)"
  type = object({
    nat_per_az          = bool
    api                 = object({ cpu = number, memory = number, min = number, max = number })
    worker              = object({ cpu = number, memory = number, min = number, max = number })
    beat                = object({ cpu = number, memory = number })
    db_instance_class   = string
    db_multi_az         = bool
    db_backup_days      = number
    redis_node_type     = string
    redis_nodes         = number
    deletion_protection = bool
  })
}
