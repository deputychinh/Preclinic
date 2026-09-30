variable "name" {
  type = string
}

variable "deletion_window_days" {
  description = "Days before a scheduled-for-deletion key is actually deleted (7-30)"
  type        = number
  default     = 30
}
