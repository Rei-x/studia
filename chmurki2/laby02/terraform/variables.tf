variable "aws_region" {
  description = "AWS region to deploy resources to"
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
  description = "List of availability zones to use for subnets"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

variable "rabbitmq_url" {
  description = "Connection string for the existing RabbitMQ server"
  type        = string
  sensitive   = true
  default     = "amqp://guest:guest@localhost:5672"
}

variable "services" {
  description = "Configuration for each microservice"
  type = map(object({
    container_port = number
    host_port      = number
    cpu            = number
    memory         = number
    image          = string
    database_url   = optional(string)
  }))
  default = {
    "meeting-service" = {
      container_port = 3000
      host_port      = 3000
      cpu            = 256
      memory         = 512
      image          = "meeting-service:latest"
      database_url   = "postgresql://postgres:postgres@localhost:5432/meeting_service_db"
    },
    "notification-service" = {
      container_port = 3001
      host_port      = 3001
      cpu            = 256
      memory         = 512
      image          = "notification-service:latest"
      database_url   = "postgresql://postgres:postgres@localhost:5432/notification_service_db"
    },
    "recording-service" = {
      container_port = 3002
      host_port      = 3002
      cpu            = 256
      memory         = 512
      image          = "recording-service:latest"
      database_url   = "postgresql://postgres:postgres@localhost:5432/recording_service_db"
    },
    "summary-service" = {
      container_port = 3003
      host_port      = 3003
      cpu            = 256
      memory         = 512
      image          = "summary-service:latest"
      database_url   = "postgresql://postgres:postgres@localhost:5432/summary_service_db"
    },
    "transcription-service" = {
      container_port = 3004
      host_port      = 3004
      cpu            = 256
      memory         = 512
      image          = "transcription-service:latest"
      database_url   = "postgresql://postgres:postgres@localhost:5432/transcription_service_db"
    }
  }
}
