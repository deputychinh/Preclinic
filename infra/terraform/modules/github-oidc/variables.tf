variable "name" {
  type = string
}

variable "repository" {
  description = "owner/name of the GitHub repository"
  type        = string
}

variable "allowed_refs" {
  type    = list(string)
  default = ["refs/heads/master", "refs/tags/v*"]
}

variable "create_provider" {
  description = "The OIDC provider exists once per account; create it only in the first environment"
  type        = bool
  default     = true
}

variable "ecr_repository_arns" {
  type = list(string)
}

variable "task_role_arns" {
  description = "Execution and task roles the deploy may pass to new task definitions"
  type        = list(string)
}

variable "ssm_path" {
  type = string
}

variable "assets_bucket_arn" {
  type = string
}
