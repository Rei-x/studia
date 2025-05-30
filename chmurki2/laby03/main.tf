# Konfiguracja providerów
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.0"
    }
    null = {
      source  = "hashicorp/null"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Zmienne
variable "aws_region" {
  description = "Region AWS"
  type        = string
  default     = "us-east-1"
}

variable "bucket_name" {
  description = "Nazwa S3 bucket"
  type        = string
  default     = "qr-generator-bucket-unique-12345"
}

variable "lambda_function_name" {
  description = "Nazwa funkcji Lambda"
  type        = string
  default     = "qr-generator"
}

# S3 Bucket do przechowywania kodów QR
resource "aws_s3_bucket" "qr_bucket" {
  bucket = var.bucket_name
}

# Konfiguracja właściciela bucket - pozwalamy na ACL dla publicznego dostępu
resource "aws_s3_bucket_ownership_controls" "qr_bucket_ownership" {
  bucket = aws_s3_bucket.qr_bucket.id

  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

# Konfiguracja publicznego dostępu do bucket
resource "aws_s3_bucket_public_access_block" "qr_bucket_pab" {
  bucket = aws_s3_bucket.qr_bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false

  depends_on = [aws_s3_bucket_ownership_controls.qr_bucket_ownership]
}

# Policy dla publicznego dostępu do plików
resource "aws_s3_bucket_policy" "qr_bucket_policy" {
  bucket = aws_s3_bucket.qr_bucket.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.qr_bucket.arn}/*"
      },
    ]
  })

  depends_on = [aws_s3_bucket_public_access_block.qr_bucket_pab]
}

# Używamy istniejącej roli LabRole dla konta edukacyjnego
variable "lab_role_arn" {
  description = "ARN roli LabRole dla konta edukacyjnego AWS"
  type        = string
  default     = "arn:aws:iam::091492946242:role/LabRole"
}

# Skrypt budowania Lambda
resource "null_resource" "build_lambda" {
  triggers = {
    lambda_code_hash  = filebase64sha256("lambda_function/lambda_function.py")
    requirements_hash = filebase64sha256("lambda_function/requirements.txt")
  }

  provisioner "local-exec" {
    command = "./build_lambda.sh"
  }
}


# Funkcja Lambda
resource "aws_lambda_function" "qr_generator" {
  filename         = "lambda_function.zip"
  function_name    = var.lambda_function_name
  role             = var.lab_role_arn
  handler          = "lambda_function.lambda_handler"
  source_code_hash = filebase64sha256("lambda_function.zip")
  runtime          = "python3.10"
  timeout          = 30
  memory_size      = 256

  environment {
    variables = {
      BUCKET_NAME = aws_s3_bucket.qr_bucket.bucket
    }
  }

  depends_on = [
    null_resource.build_lambda,
  ]
}

# URL funkcji Lambda
resource "aws_lambda_function_url" "qr_generator_url" {
  function_name      = aws_lambda_function.qr_generator.function_name
  authorization_type = "NONE"

  cors {
    allow_credentials = false
    allow_methods     = ["POST"]
    allow_origins     = ["*"]
    allow_headers     = ["date", "keep-alive", "content-type"]
    expose_headers    = ["date", "keep-alive"]
    max_age           = 86400
  }
}

# Outputs
output "lambda_function_url" {
  description = "URL funkcji Lambda"
  value       = aws_lambda_function_url.qr_generator_url.function_url
}

output "s3_bucket_name" {
  description = "Nazwa S3 bucket"
  value       = aws_s3_bucket.qr_bucket.bucket
}

output "s3_bucket_domain" {
  description = "Publiczny URL S3 bucket"
  value       = "https://${aws_s3_bucket.qr_bucket.bucket}.s3.amazonaws.com"
}
