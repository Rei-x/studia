#!/bin/bash

# deploy.sh - Skrypt automatycznego wdrożenia generatora QR

set -e

echo "🚀 Rozpoczynanie wdrożenia generatora kodów QR..."

# Sprawdzenie wymagań
if ! command -v terraform &>/dev/null; then
  echo "❌ Terraform nie jest zainstalowany"
  exit 1
fi

if ! command -v aws &>/dev/null; then
  echo "❌ AWS CLI nie jest zainstalowany"
  exit 1
fi

if ! command -v python3 &>/dev/null; then
  echo "❌ Python3 nie jest zainstalowany"
  exit 1
fi

if ! command -v pip3 &>/dev/null; then
  echo "❌ pip3 nie jest zainstalowany"
  exit 1
fi

# Sprawdzenie konfiguracji AWS
echo "🔍 Sprawdzanie konfiguracji AWS..."
if ! aws sts get-caller-identity &>/dev/null; then
  echo "❌ AWS CLI nie jest skonfigurowane. Uruchom: aws configure"
  exit 1
fi

echo "✅ AWS skonfigurowane poprawnie"

# Sprawdzenie czy istnieje terraform.tfvars
if [ ! -f "terraform.tfvars" ]; then
  echo "⚠️  Plik terraform.tfvars nie istnieje"
  echo "📋 Kopiuję przykładowy plik..."
  cp terraform.tfvars.example terraform.tfvars
  echo "📝 Edytuj plik terraform.tfvars i ustaw unikalną nazwę bucket, następnie uruchom skrypt ponownie"
  exit 1
fi

# Inicjalizacja Terraform
echo "🔧 Inicjalizacja Terraform..."
terraform init

# Walidacja konfiguracji
echo "✅ Walidacja konfiguracji Terraform..."
terraform validate

# Plan wdrożenia
echo "📋 Generowanie planu wdrożenia..."
terraform plan -out=tfplan

# Potwierdzenie wdrożenia
echo ""
echo "🤔 Czy chcesz kontynuować wdrożenie? (tak/nie)"
read -r response
if [[ "$response" != "tak" ]]; then
  echo "❌ Wdrożenie anulowane"
  rm -f tfplan
  exit 0
fi

# Wdrożenie
echo "🚀 Wdrażanie infrastruktury..."
terraform apply tfplan

# Usunięcie planu
rm -f tfplan

# Pobieranie outputów
echo ""
echo "📊 Podsumowanie wdrożenia:"
echo "========================="
echo "🔗 URL funkcji Lambda:"
terraform output lambda_function_url

echo ""
echo "🪣 Nazwa S3 Bucket:"
terraform output s3_bucket_name

echo ""
echo "🌐 Publiczny URL S3:"
terraform output s3_bucket_domain

# Test podstawowy
LAMBDA_URL=$(terraform output -raw lambda_function_url)
echo ""
echo "🧪 Wykonywanie testu podstawowego..."

TEST_RESPONSE=$(curl -s -X POST "$LAMBDA_URL" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com"}')

if echo "$TEST_RESPONSE" | grep -q '"success": true'; then
  echo "✅ Test podstawowy zakończony sukcesem!"
  QR_URL=$(echo "$TEST_RESPONSE" | grep -o 'https://[^"]*\.png')
  echo "🖼️  Przykładowy kod QR: $QR_URL"
else
  echo "❌ Test podstawowy nie powiódł się:"
  echo "$TEST_RESPONSE"
fi

echo ""
echo "🎉 Wdrożenie zakończone!"
echo ""
echo "📚 Następne kroki:"
echo "1. Sprawdź README.md w celu poznania sposobów użycia"
echo "2. Zobacz examples.md dla przykładów testowania"
echo "3. Użyj curl lub innych narzędzi do testowania API"
echo ""
echo "🧹 Aby usunąć infrastrukturę, uruchom: terraform destroy"
