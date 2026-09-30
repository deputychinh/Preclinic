variable "name" {
  description = "Service, task family and log group name, e.g. carepath-staging-api"
  type        = string
}

variable "container_name" {
  type = string
}

variable "image" {
  description = "Initial image; later rollouts come from scripts/aws/deploy.sh"
  type        = string
}

variable "command" {
  description = "Override CMD — used to run the same image as api/worker/beat (plan §15.3)"
  type        = list(string)
  default     = null
}

variable "port" {
  description = "null for a service with no inbound traffic (worker, beat)"
  type        = number
  default     = null
}

variable "cpu" {
  type    = number
  default = 256
}

variable "memory" {
  type    = number
  default = 512
}

variable "min_count" {
  type    = number
  default = 1
}

variable "max_count" {
  type    = number
  default = 2
}

variable "cpu_target_percent" {
  type    = number
  default = 60
}

variable "cluster_arn" {
  type = string
}

variable "cluster_name" {
  type = string
}

variable "namespace_arn" {
  type = string
}

variable "service_connect_alias" {
  description = "DNS name other services use (e.g. \"api\"); null for a service nothing calls directly"
  type        = string
  default     = null
}

variable "subnet_ids" {
  type = list(string)
}

variable "security_group_id" {
  type = string
}

variable "target_group_arn" {
  description = "null for a service with no ALB target group (worker, beat — plan §15.3)"
  type        = string
  default     = null
}

variable "environment" {
  type    = map(string)
  default = {}
}

variable "secrets" {
  description = "Env var name → Secrets Manager ARN (optionally with :json-key::)"
  type        = map(string)
  default     = {}
}

variable "secret_arns" {
  description = "Secret ARNs the execution role may read"
  type        = list(string)
  default     = []
}

variable "task_policy_json" {
  description = "Optional inline IAM policy JSON for the task role (e.g. worker's S3 lab-import access)"
  type        = string
  default     = null
}

variable "log_retention_days" {
  type    = number
  default = 30
}
