output "cluster_id" {
  description = "The ID of the ECS cluster"
  value       = aws_ecs_cluster.main.id
}

output "cluster_name" {
  description = "The name of the ECS cluster"
  value       = aws_ecs_cluster.main.name
}

output "service_names" {
  description = "Names of the ECS services"
  value       = [for svc in aws_ecs_service.service : svc.name]
}

output "ecr_repository_urls" {
  description = "The URLs of the ECR repositories"
  value = {
    for key, repo in aws_ecr_repository.service : key => repo.repository_url
  }
}

output "service_load_balancer_dns" {
  description = "The DNS names of each service's load balancer"
  value = {
    for key, lb in aws_lb.service : key => lb.dns_name
  }
}

output "service_load_balancer_urls" {
  description = "HTTP URLs for each service"
  value = {
    for key, lb in aws_lb.service : key => "http://${lb.dns_name}"
  }
}
