terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.2.0"
}

provider "aws" {
  region = var.aws_region
}

# Load modules
module "network" {
  source = "./modules/network"

  project_name       = var.project_name
  vpc_cidr           = var.vpc_cidr
  availability_zones = var.availability_zones
}

module "ecs" {
  source = "./modules/ecs"

  project_name                = var.project_name
  vpc_id                      = module.network.vpc_id
  public_subnet_ids           = module.network.public_subnet_ids
  private_subnet_ids          = module.network.private_subnet_ids
  lb_security_group_id        = module.network.lb_security_group_id
  ecs_tasks_security_group_id = module.network.ecs_tasks_security_group_id

  # Pass your existing database and RabbitMQ connections as environment variables
  database_url = var.database_url
  rabbitmq_url = var.rabbitmq_url

  # Use existing ECS Task Execution Role in education account
  execution_role_arn = "arn:aws:iam::091492946242:role/LabRole"
  task_role_arn      = "arn:aws:iam::091492946242:role/LabRole"
}
