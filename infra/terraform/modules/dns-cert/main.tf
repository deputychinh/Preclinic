# DNS-validated certificates: one in us-east-1 for CloudFront (public domain), one in the region
# for the ALB (origin domain). The hosted zone must already exist in Route 53.

data "aws_route53_zone" "this" {
  name         = var.zone_name
  private_zone = false
}

resource "aws_acm_certificate" "cloudfront" {
  provider          = aws.us_east_1
  domain_name       = var.domain
  validation_method = "DNS"
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_acm_certificate" "origin" {
  domain_name       = var.origin_domain
  validation_method = "DNS"
  lifecycle {
    create_before_destroy = true
  }
}

locals {
  validation_options = {
    for option in concat(
      tolist(aws_acm_certificate.cloudfront.domain_validation_options),
      tolist(aws_acm_certificate.origin.domain_validation_options),
    ) : option.domain_name => option
  }
}

resource "aws_route53_record" "validation" {
  for_each        = local.validation_options
  zone_id         = data.aws_route53_zone.this.zone_id
  name            = each.value.resource_record_name
  type            = each.value.resource_record_type
  records         = [each.value.resource_record_value]
  ttl             = 300
  allow_overwrite = true
}

resource "aws_acm_certificate_validation" "cloudfront" {
  provider                = aws.us_east_1
  certificate_arn         = aws_acm_certificate.cloudfront.arn
  validation_record_fqdns = [aws_route53_record.validation[var.domain].fqdn]
}

resource "aws_acm_certificate_validation" "origin" {
  certificate_arn         = aws_acm_certificate.origin.arn
  validation_record_fqdns = [aws_route53_record.validation[var.origin_domain].fqdn]
}
