output "zone_id" {
  value = data.aws_route53_zone.this.zone_id
}

output "cloudfront_certificate_arn" {
  value = aws_acm_certificate_validation.cloudfront.certificate_arn
}

output "origin_certificate_arn" {
  value = aws_acm_certificate_validation.origin.certificate_arn
}
