variable "path" {
  description = "e.g. /carepath/staging/deploy"
  type        = string
}

variable "parameters" {
  type = map(string)
}
