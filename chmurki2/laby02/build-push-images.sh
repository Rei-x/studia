#!/bin/bash

# Script to build and push Docker images to a single AWS ECR repository
# Make sure you have AWS CLI installed and configured with appropriate credentials

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

PROJECT_NAME="meeting-app"

# Get AWS account ID
echo -e "${YELLOW}Getting AWS Account ID...${NC}"
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

if [ $? -ne 0 ]; then
  echo -e "${RED}Failed to get AWS account ID. Make sure your AWS CLI is properly configured.${NC}"
  exit 1
fi

echo -e "${GREEN}AWS Account ID: ${AWS_ACCOUNT_ID}${NC}"

# Create or check ECR repository
REPO_NAME="${PROJECT_NAME}-repo"
ECR_URI="$AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/$REPO_NAME"

echo -e "${YELLOW}Logging in to Amazon ECR...${NC}"
# Get the login token
ECR_TOKEN=$(aws ecr get-login-password --region us-east-1)
if [ $? -ne 0 ]; then
  echo -e "${RED}Failed to get ECR token. Check your AWS credentials.${NC}"
  exit 1
fi

# Login without using the default Docker credential helper
echo "$ECR_TOKEN" | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
if [ $? -ne 0 ]; then
  echo -e "${RED}Failed to log in to ECR.${NC}"
  exit 1
fi

# Services to build and push
SERVICES=(
  "meeting-service"
  "notification-service"
  "recording-service"
  "summary-service"
  "transcription-service"
)

# Build and push each service to the same repository but with different tags
for SERVICE in "${SERVICES[@]}"; do
  echo -e "${YELLOW}Processing service: ${SERVICE}${NC}"
  SERVICE_DIR="./${SERVICE}"

  REPO_URI="${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/meeting-app-${SERVICE}-repo-v2"

  echo -e "${YELLOW}Building Docker image for ${SERVICE}...${NC}"
  TAG="latest"

  docker build -t $REPO_URI:$TAG -f ${SERVICE_DIR}/Dockerfile ${SERVICE_DIR}

  if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to build Docker image for ${SERVICE}.${NC}"
    continue
  fi

  # Push the image to ECR
  echo -e "${YELLOW}Pushing Docker image for ${SERVICE} to ECR...${NC}"
  docker push $REPO_URI:$TAG

  if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to push Docker image for ${SERVICE}.${NC}"
    continue
  fi

  echo -e "${GREEN}Successfully built and pushed ${SERVICE} to ECR.${NC}"
  echo -e "${GREEN}Image URI: ${REPO_URI}:${TAG}${NC}"
done

echo -e "${GREEN}All services processed.${NC}"
echo -e "${YELLOW}Next steps:${NC}"
echo -e "${YELLOW}1. Run 'cd terraform && terraform apply' to deploy infrastructure using these images${NC}"
echo -e "${YELLOW}2. Your services will be accessible through the AWS load balancer${NC}"
