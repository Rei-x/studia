############### ECS Cluster ###############

resource "aws_ecs_cluster" "main" {
  name = "${var.project_name}-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = {
    Name = "${var.project_name}-cluster"
  }
}

############### ECR Repositories ###############

# Create a separate ECR repository for each service
resource "aws_ecr_repository" "service" {
  for_each = var.services

  name                 = "${var.project_name}-${each.key}-repo-v2"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "${var.project_name}-${each.key}-repo-v2"
  }
}

############### Load Balancers ###############

# Create a separate load balancer for each service
resource "aws_lb" "service" {
  for_each = var.services

  name               = "${substr(var.project_name, 0, 16)}-${substr(each.key, 0, 16)}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [var.lb_security_group_id]
  subnets            = var.public_subnet_ids # Using all public subnets across AZs

  enable_deletion_protection = false

  tags = {
    Name = "${var.project_name}-${each.key}-alb"
  }
}

resource "aws_lb_target_group" "service" {
  for_each = var.services

  name        = "${substr(var.project_name, 0, 16)}-${substr(each.key, 0, 16)}-tg"
  port        = each.value.container_port
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip"

  health_check {
    healthy_threshold   = 3
    interval            = 30
    protocol            = "HTTP"
    matcher             = "200"
    timeout             = 5
    path                = "/health"
    unhealthy_threshold = 3
  }

  tags = {
    Name = "${var.project_name}-${each.key}-tg"
  }
}

resource "aws_lb_listener" "service" {
  for_each = var.services

  load_balancer_arn = aws_lb.service[each.key].arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.service[each.key].arn
  }

  tags = {
    Name = "${var.project_name}-${each.key}-listener"
  }
}

############### CloudWatch Log Groups ###############

resource "aws_cloudwatch_log_group" "service" {
  for_each = var.services

  name              = "/ecs/${var.project_name}/${each.key}"
  retention_in_days = 30

  tags = {
    Name = "${var.project_name}-${each.key}-logs"
  }
}

############### ECS Task Definitions ###############

# Use locals to determine role ARNs based on provided variables or default to the AmazonECSTaskExecutionRolePolicy
locals {
  # Default execution role ARN if none provided (using AWS-managed role)
  default_execution_role_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"

  # Use provided role ARNs or defaults
  execution_role_arn = var.execution_role_arn != "" ? var.execution_role_arn : local.default_execution_role_arn
  task_role_arn      = var.task_role_arn != "" ? var.task_role_arn : local.default_execution_role_arn
}

resource "aws_ecs_task_definition" "service" {
  for_each = var.services

  family                   = "${var.project_name}-${each.key}"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = each.value.cpu
  memory                   = each.value.memory
  execution_role_arn       = local.execution_role_arn
  task_role_arn            = local.task_role_arn

  container_definitions = jsonencode([
    {
      name      = each.key
      image     = "${aws_ecr_repository.service[each.key].repository_url}:latest"
      essential = true

      portMappings = [
        {
          containerPort = each.value.container_port
          hostPort      = each.value.container_port
        }
      ]

      environment = [
        {
          name  = "DATABASE_URL"
          value = lookup(each.value, "database_url", "")
        },
        {
          name  = "RABBIT_MQ_URL"
          value = var.rabbitmq_url
        },
        {
          name  = "SERVICE_NAME"
          value = each.key
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.service[each.key].name
          "awslogs-region"        = data.aws_region.current.name
          "awslogs-stream-prefix" = "ecs"
        }
      }
    }
  ])

  tags = {
    Name = "${var.project_name}-${each.key}-task-definition"
  }
}

############### ECS Services ###############

resource "aws_ecs_service" "service" {
  for_each = var.services

  name                              = each.key
  cluster                           = aws_ecs_cluster.main.id
  task_definition                   = aws_ecs_task_definition.service[each.key].arn
  desired_count                     = 1
  launch_type                       = "FARGATE"
  scheduling_strategy               = "REPLICA"
  health_check_grace_period_seconds = 60
  force_new_deployment              = true

  network_configuration {
    subnets          = var.private_subnet_ids
    security_groups  = [var.ecs_tasks_security_group_id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.service[each.key].arn
    container_name   = each.key
    container_port   = each.value.container_port
  }

  depends_on = [
    aws_lb_listener.service
  ]

  tags = {
    Name = "${var.project_name}-${each.key}-service"
  }
}

############### Data Sources ###############

data "aws_region" "current" {}
data "aws_caller_identity" "current" {}
