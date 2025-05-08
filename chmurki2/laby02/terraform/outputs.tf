output "vpc_id" {
  description = "The ID of the VPC"
  value       = module.network.vpc_id
}

output "service_load_balancer_dns" {
  description = "The DNS names of each service's load balancer"
  value       = module.ecs.service_load_balancer_dns
}

output "service_load_balancer_urls" {
  description = "HTTP URLs for each service"
  value       = module.ecs.service_load_balancer_urls
}

output "ecs_cluster_name" {
  description = "Name of the ECS cluster"
  value       = module.ecs.cluster_name
}

output "ecs_service_names" {
  description = "Names of the ECS services"
  value       = module.ecs.service_names
}

