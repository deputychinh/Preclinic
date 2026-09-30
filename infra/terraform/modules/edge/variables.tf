variable "name" {
  type = string
}

variable "domain" {
  description = "Public domain, e.g. staging.example.com"
  type        = string
}

variable "origin_domain" {
  description = "Domain that points at the ALB, e.g. origin-staging.example.com"
  type        = string
}

variable "certificate_arn" {
  description = "ACM certificate in us-east-1 for the public domain"
  type        = string
}

variable "assets_bucket_domain_name" {
  type = string
}

variable "origin_verify_secret" {
  type      = string
  sensitive = true
}

variable "price_class" {
  type    = string
  default = "PriceClass_200" # includes Asia
}

variable "rate_limit_per_5_minutes" {
  type    = number
  default = 2000
}
