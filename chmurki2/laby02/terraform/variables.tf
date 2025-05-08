variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "meeting-app"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "List of availability zones to use"
  type        = list(string)
  default     = ["eu-west-1a", "eu-west-1b"]
}

variable "database_url" {
  description = "Connection string for the existing PostgreSQL database"
  type        = string
  sensitive   = true
}

variable "rabbitmq_url" {
  description = "Connection string for the existing RabbitMQ server"
  type        = string
  sensitive   = true
}

variable "services" {
  description = "Configuration for each microservice"
  type = map(object({
    container_port = number
    host_port      = number
    cpu            = number
    memory         = number
    image          = string
  }))
  default = {
    "meeting-service" = {
      container_port = 3000
      host_port      = 3000
      cpu            = 256
      memory         = 512
      image          = "meeting-service:latest"
    },
    "notification-service" = {
      container_port = 3001
      host_port      = 3001
      cpu            = 256
      memory         = 512
      image          = "notification-service:latest"
    },
    "recording-service" = {
      container_port = 3002
      host_port      = 3002
      cpu            = 256
      memory         = 512
      image          = "recording-service:latest"
    },
    "summary-service" = {
      container_port = 3003
      host_port      = 3003
      cpu            = 256
      memory         = 512
      image          = "summary-service:latest"
    },
    "transcription-service" = {
      container_port = 3004
      host_port      = 3004
      cpu            = 256
      memory         = 512
      image          = "transcription-service:latest"
    }
  }
}
