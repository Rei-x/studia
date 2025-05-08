output "vpc_id" {
  description = "The ID of the VPC"
  value       = module.network.vpc_id
}

output "load_balancer_dns" {
  description = "The DNS name of the load balancer"
  value       = module.ecs.load_balancer_dns
}

output "ecs_cluster_name" {
  description = "Name of the ECS cluster"
  value       = module.ecs.cluster_name
}

output "ecs_service_names" {
  description = "Names of the ECS services"
  value       = module.ecs.service_names
}

output "ecr_repository_url" {
  description = "URL of the ECR repository for Docker image pushing"
  value       = module.ecs.ecr_repository_url
}
