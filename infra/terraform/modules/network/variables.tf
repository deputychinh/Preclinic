variable "name" {
  description = "Name prefix, e.g. carepath-staging"
  type        = string
}

variable "cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"
}

variable "azs" {
  description = "Availability zones (at least two)"
  type        = list(string)
  validation {
    condition     = length(var.azs) >= 2
    error_message = "Use at least two availability zones."
  }
}

variable "nat_per_az" {
  description = "One NAT gateway per AZ (true in production) or a single shared one"
  type        = bool
  default     = false
}
