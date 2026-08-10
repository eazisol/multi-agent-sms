variable "environment_name" {
  type        = string
  description = "Environment name: staging or production"
  validation {
    condition     = contains(["staging", "production"], var.environment_name)
    error_message = "environment_name must be staging or production."
  }
}

variable "org_short_name" {
  type        = string
  description = "Organization short name used for resource naming"
  default     = "masms"
}

variable "aws_region" {
  type        = string
  description = "AWS region"
  default     = "us-east-1"
}
