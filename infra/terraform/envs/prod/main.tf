terraform {
  required_version = ">= 1.6"
  # Partial config: bucket and key come from backend.hcl (created by scripts/aws/bootstrap.sh).
  backend "s3" {}
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.80"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }
}

locals {
  tags = {
    Project     = var.project
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

provider "aws" {
  region = var.region
  default_tags {
    tags = local.tags
  }
}

provider "aws" {
  alias  = "us_east_1"
  region = "us-east-1"
  default_tags {
    tags = local.tags
  }
}

module "stack" {
  source                      = "../../stack"
  project                     = var.project
  environment                 = var.environment
  azs                         = var.azs
  vpc_cidr                    = var.vpc_cidr
  zone_name                   = var.zone_name
  domain                      = var.domain
  github_repository           = var.github_repository
  create_github_oidc_provider = var.create_github_oidc_provider
  alert_email                 = var.alert_email
  monthly_budget_usd          = var.monthly_budget_usd
  anthropic_api_key           = var.anthropic_api_key
  sizing                      = var.sizing
  providers = {
    aws           = aws
    aws.us_east_1 = aws.us_east_1
  }
}
