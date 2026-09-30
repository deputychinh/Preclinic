variable "project" {
  type    = string
  default = "carepath"
}

variable "environment" {
  type = string
}

variable "region" {
  type    = string
  default = "ap-southeast-1"
}

variable "azs" {
  type = list(string)
}

variable "vpc_cidr" {
  type = string
}

variable "zone_name" {
  type = string
}

variable "domain" {
  type = string
}

variable "github_repository" {
  type = string
}

variable "create_github_oidc_provider" {
  type = bool
}

variable "alert_email" {
  type = string
}

variable "monthly_budget_usd" {
  type = number
}

variable "anthropic_api_key" {
  type      = string
  sensitive = true
}

variable "sizing" {
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
