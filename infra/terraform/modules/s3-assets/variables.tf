variable "bucket_name" {
  type = string
}

variable "force_destroy" {
  type    = bool
  default = false
}

variable "kms_key_id" {
  description = "Customer-managed KMS key ARN — set for the lab-import bucket (PHI), leave null for the SPA-assets bucket (plan §6.10/§15.4)"
  type        = string
  default     = null
}
