terraform {
  required_providers {
    aws = {
      source                = "hashicorp/aws"
      configuration_aliases = [aws.us_east_1] # CloudFront certificates must be in us-east-1
    }
  }
}
