# Production: two tasks minimum for the API, NAT per AZ, Multi-AZ database, Redis replica (plan §15.5).
# Worker stays at 1 task (Celery scales by concurrency, not replica count, for this workload size);
# beat is always exactly 1 (singleton, plan §15.4).
environment                 = "prod"
azs                         = ["ap-southeast-1a", "ap-southeast-1b"]
vpc_cidr                    = "10.21.0.0/16"
zone_name                   = "example.com"              # replace
domain                      = "app.carepath.example.com" # replace
github_repository           = "your-org/carepath"        # replace
create_github_oidc_provider = false                      # already created by staging in the same account
alert_email                 = "alerts@example.com"       # replace
monthly_budget_usd          = 480
anthropic_api_key           = "REPLACE_ME"

sizing = {
  nat_per_az          = true
  api                 = { cpu = 512, memory = 1024, min = 2, max = 6 }
  worker              = { cpu = 512, memory = 1024, min = 1, max = 2 }
  beat                = { cpu = 256, memory = 512 }
  db_instance_class   = "db.t4g.small"
  db_multi_az         = true
  db_backup_days      = 14
  redis_node_type     = "cache.t4g.small"
  redis_nodes         = 2
  deletion_protection = true
}
