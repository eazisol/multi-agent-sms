terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

locals {
  name_prefix = "${var.org_short_name}-${var.environment_name}"
  common_tags = {
    Environment = var.environment_name
    Module      = "MOD-030"
    ManagedBy   = "terraform-skeleton"
  }
}

resource "aws_secretsmanager_secret" "app" {
  name                    = "${local.name_prefix}/app"
  description             = "MASMS application secrets placeholder (${var.environment_name})"
  recovery_window_in_days = var.environment_name == "production" ? 30 : 0
  tags                    = local.common_tags
}

output "secrets_manager_arn" {
  value       = aws_secretsmanager_secret.app.arn
  description = "Primary Secrets Manager secret ARN (values must be set out-of-band)"
}

output "name_prefix" {
  value = local.name_prefix
}
