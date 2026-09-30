variable "zone_name" {
  description = "Route 53 hosted zone, e.g. example.com"
  type        = string
}

variable "domain" {
  type = string
}

variable "origin_domain" {
  type = string
}
