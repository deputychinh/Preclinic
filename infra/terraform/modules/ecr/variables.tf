variable "project" {
  type = string
}

variable "services" {
  type    = list(string)
  default = ["backend", "frontend"]
}

variable "keep_images" {
  type    = number
  default = 20
}

variable "force_delete" {
  description = "Allow destroying repositories that still hold images (staging only)"
  type        = bool
  default     = false
}
