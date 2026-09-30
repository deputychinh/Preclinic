variable "name" {
  type = string
}

variable "vpc_id" {
  type = string
}

variable "subnet_ids" {
  type = list(string)
}

variable "security_group_id" {
  type = string
}

variable "certificate_arn" {
  description = "Regional ACM certificate for the origin domain"
  type        = string
}

variable "origin_verify_secret" {
  type      = string
  sensitive = true
}

variable "deletion_protection" {
  type    = bool
  default = false
}
