output "site_url" {
  value = local.site_url
}

output "cloudfront_domain" {
  value = module.edge.domain_name
}

output "alb_dns_name" {
  value = module.alb.dns_name
}

output "ecr_repositories" {
  value = module.ecr.repository_urls
}

output "cluster_name" {
  value = module.cluster.cluster_name
}

output "lab_imports_bucket" {
  value = module.lab_imports.bucket_name
}

output "kms_key_arn" {
  value = module.kms.key_arn
}

output "github_deploy_role_arn" {
  description = "Set as the AWS_DEPLOY_ROLE_ARN variable of the GitHub environment"
  value       = module.github_oidc.role_arn
}

output "alerts_topic_arn" {
  value = module.monitoring.alerts_topic_arn
}
