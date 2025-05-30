#!/bin/bash

STACK_NAME="microservices-stack"

echo "Initializing Docker Swarm (if not already initialized)..."
docker swarm init 2>/dev/null || echo "Swarm already initialized"

echo "Ensuring manager node can run workloads..."
docker node update --availability active $(docker node ls --format "{{.Hostname}}" --filter "role=manager")

echo "Deploying stack to Docker Swarm..."
docker stack deploy -c docker-stack.yml $STACK_NAME

echo "Waiting for services to start..."
sleep 15

echo "Detailed service info:"
docker stack services $STACK_NAME

sleep 10

docker service scale "$STACK_NAME"_notification-service=3
echo "Scaled up notification-service to 3 instances"
sleep 10
docker service scale "$STACK_NAME"_notification-service=2
echo "Scaled down notification-service to 2 instances"
sleep 10

echo "Removing stack..."
docker stack rm $STACK_NAME
