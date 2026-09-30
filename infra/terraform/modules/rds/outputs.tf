output "endpoint" {
  description = "host:port"
  value       = aws_db_instance.this.endpoint
}

output "identifier" {
  value = aws_db_instance.this.identifier
}

output "database" {
  value = aws_db_instance.this.db_name
}

output "username" {
  value = aws_db_instance.this.username
}
