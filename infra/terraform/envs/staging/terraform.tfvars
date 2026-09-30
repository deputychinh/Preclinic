# Staging: smallest sizes, single NAT, no Multi-AZ (plan §15.5).
# Extra vs. the real-estate project's staging: 2 more Fargate tasks (worker + beat) and a CMK.
environment                 = "staging"
azs                         = ["ap-southeast-1a", "ap-southeast-1b"]
vpc_cidr                    = "10.20.0.0/16"
zone_name                   = "example.com"                  # replace with your hosted zone
domain                      = "staging.carepath.example.com" # replace
github_repository           = "your-org/carepath"            # replace
create_github_oidc_provider = true
alert_email                 = "alerts@example.com" # replace
monthly_budget_usd          = 220
# anthropic_api_key: set via TF_VAR_anthropic_api_key env var or a .auto.tfvars gitignored file —
# never commit a real key.
anthropic_api_key = "REPLACE_ME"

sizing = {
  nat_per_az          = false
  api                 = { cpu = 256, memory = 512, min = 1, max = 2 }
  worker              = { cpu = 256, memory = 512, min = 1, max = 1 }
  beat                = { cpu = 256, memory = 512 }
  db_instance_class   = "db.t4g.micro"
  db_multi_az         = false
  db_backup_days      = 7
  redis_node_type     = "cache.t4g.micro"
  redis_nodes         = 1
  deletion_protection = false
}
