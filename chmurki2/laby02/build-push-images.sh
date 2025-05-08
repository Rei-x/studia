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

# Create .env files with database and RabbitMQ connection info if they don't exist
echo -e "${YELLOW}Checking/creating environment files...${NC}"

# Get DATABASE_URL and RABBIT_MQ_URL from terraform.tfvars if available
if [ -f "./terraform/terraform.tfvars" ]; then
  DATABASE_URL=$(grep "database_url" ./terraform/terraform.tfvars | cut -d'=' -f2 | tr -d ' "')
  # Remove any trailing comments if present
  DATABASE_URL=$(echo $DATABASE_URL | cut -d'#' -f1 | tr -d ' ')

  RABBIT_MQ_URL=$(grep "rabbitmq_url" ./terraform/terraform.tfvars | cut -d'=' -f2 | tr -d ' "')
  # Remove any trailing comments if present
  RABBIT_MQ_URL=$(echo $RABBIT_MQ_URL | cut -d'#' -f1 | tr -d ' ')
else
  # If not found in terraform.tfvars, prompt for them
  if [ -z "$DATABASE_URL" ]; then
    read -p "Enter DATABASE_URL: " DATABASE_URL
  fi

  if [ -z "$RABBIT_MQ_URL" ]; then
    read -p "Enter RABBIT_MQ_URL: " RABBIT_MQ_URL
  fi
fi

# Function to create environment file if it doesn't exist
create_env_file() {
  SERVICE_DIR=$1
  ENV_FILE="${SERVICE_DIR}/.env"

  if [ ! -f "$ENV_FILE" ]; then
    echo -e "${YELLOW}Creating .env file for ${SERVICE_DIR}...${NC}"
    cat >"$ENV_FILE" <<EOL
DATABASE_URL=${DATABASE_URL}
RABBIT_MQ_URL=${RABBIT_MQ_URL}
EOL
    echo -e "${GREEN}Created .env file for ${SERVICE_DIR}${NC}"
  else
    echo -e "${GREEN}.env file already exists for ${SERVICE_DIR}${NC}"
  fi
}

# Create .env files for all services
for SERVICE in "${SERVICES[@]}"; do
  create_env_file "./${SERVICE}"
done

# Build and push each service to the same repository but with different tags
for SERVICE in "${SERVICES[@]}"; do
  echo -e "${YELLOW}Processing service: ${SERVICE}${NC}"
  SERVICE_DIR="./${SERVICE}"

  # Check if Dockerfile exists in the service directory
  if [ ! -f "${SERVICE_DIR}/Dockerfile" ]; then
    echo -e "${RED}Dockerfile not found for ${SERVICE}. Skipping.${NC}"
    continue
  fi

  # Build Docker image with service-specific tag
  echo -e "${YELLOW}Building Docker image for ${SERVICE}...${NC}"
  # Tag format: repository-url:service-name-latest
  TAG="${SERVICE}-latest"

  # Build using the correct context and Dockerfile
  docker build -t $ECR_URI:$TAG -f ${SERVICE_DIR}/Dockerfile ${SERVICE_DIR}

  if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to build Docker image for ${SERVICE}.${NC}"
    continue
  fi

  # Push the image to ECR
  echo -e "${YELLOW}Pushing Docker image for ${SERVICE} to ECR...${NC}"
  docker push $ECR_URI:$TAG

  if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to push Docker image for ${SERVICE}.${NC}"
    continue
  fi

  echo -e "${GREEN}Successfully built and pushed ${SERVICE} to ECR.${NC}"
  echo -e "${GREEN}Image URI: ${ECR_URI}:${TAG}${NC}"
done

echo -e "${GREEN}All services processed.${NC}"
echo -e "${YELLOW}Next steps:${NC}"
echo -e "${YELLOW}1. Run 'cd terraform && terraform apply' to deploy infrastructure using these images${NC}"
echo -e "${YELLOW}2. Your services will be accessible through the AWS load balancer${NC}"
