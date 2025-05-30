#!/bin/bash

# test_qr_generator.sh - Kompleksowy skrypt testowy dla generatora QR

set -e

# Kolory dla outputu
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funkcja do wyświetlania kolorowych komunikatów
log_info() {
  echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
  echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
  echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
  echo -e "${RED}❌ $1${NC}"
}

# Sprawdzenie czy Terraform jest wdrożony
if [ ! -f "terraform.tfstate" ]; then
  log_error "Terraform nie został jeszcze wdrożony. Uruchom najpierw: ./deploy.sh"
  exit 1
fi

# Pobieranie URL Lambda z Terraform
log_info "Pobieranie URL funkcji Lambda..."
LAMBDA_URL=$(terraform output -raw lambda_function_url 2>/dev/null)

if [ -z "$LAMBDA_URL" ]; then
  log_error "Nie udało się pobrać URL funkcji Lambda"
  exit 1
fi

log_success "URL funkcji Lambda: $LAMBDA_URL"

# Funkcja do testowania pojedynczego przypadku
test_case() {
  local test_name="$1"
  local payload="$2"
  local expected_status="$3"

  log_info "Test: $test_name"

  response=$(curl -s -w "\n%{http_code}" -X POST "$LAMBDA_URL" \
    -H "Content-Type: application/json" \
    -d "$payload")

  http_code=$(echo "$response" | tail -n1)
  body=$(echo "$response" | head -n -1)

  if [ "$http_code" = "$expected_status" ]; then
    log_success "Status HTTP: $http_code ✓"

    # Sprawdzenie czy odpowiedź zawiera prawidłowy JSON
    if echo "$body" | jq . >/dev/null 2>&1; then
      log_success "Prawidłowy JSON ✓"

      # Wyświetlenie kluczowych informacji
      if [ "$expected_status" = "200" ]; then
        success=$(echo "$body" | jq -r '.success // false')
        if [ "$success" = "true" ]; then
          qr_url=$(echo "$body" | jq -r '.qr_image_url // "N/A"')
          original_url=$(echo "$body" | jq -r '.original_url // "N/A"')
          log_success "QR wygenerowany dla: $original_url"
          log_success "Link do QR: $qr_url"
        else
          log_warning "Funkcja zwróciła success: false"
        fi
      else
        error_msg=$(echo "$body" | jq -r '.error // "N/A"')
        log_info "Oczekiwany błąd: $error_msg"
      fi
    else
      log_error "Nieprawidłowy JSON w odpowiedzi"
    fi
  else
    log_error "Nieprawidłowy status HTTP: $http_code (oczekiwano: $expected_status)"
  fi

  echo "Odpowiedź:"
  echo "$body" | jq . 2>/dev/null || echo "$body"
  echo "----------------------------------------"
  echo
}

# Uruchomienie testów
echo "🧪 Rozpoczynanie kompleksowych testów generatora QR"
echo "=================================================="
echo

# Test 1: Prawidłowy URL z protokołem HTTPS
test_case "Prawidłowy URL HTTPS" \
  '{"url": "https://github.com"}' \
  "200"

# Test 2: Prawidłowy URL z protokołem HTTP
test_case "Prawidłowy URL HTTP" \
  '{"url": "http://example.com"}' \
  "200"

# Test 3: URL bez protokołu
test_case "URL bez protokołu" \
  '{"url": "google.com"}' \
  "200"

# Test 4: URL z www bez protokołu
test_case "URL z www bez protokołu" \
  '{"url": "www.stackoverflow.com"}' \
  "200"

# Test 5: Długi URL z parametrami
test_case "Długi URL z parametrami" \
  '{"url": "https://stackoverflow.com/questions/tagged/aws-lambda?tab=Votes&pagesize=50&sort=votes"}' \
  "200"

# Test 6: URL z polskimi znakami
test_case "URL z polskimi znakami" \
  '{"url": "https://pl.wikipedia.org/wiki/Chmura_obliczeniowa"}' \
  "200"

# Test 7: Brak parametru URL
test_case "Brak parametru URL" \
  '{}' \
  "400"

# Test 8: Pusty URL
test_case "Pusty URL" \
  '{"url": ""}' \
  "400"

# Test 9: Nieprawidłowy JSON
log_info "Test: Nieprawidłowy JSON"
response=$(curl -s -w "\n%{http_code}" -X POST "$LAMBDA_URL" \
  -H "Content-Type: application/json" \
  -d '{"url":')

http_code=$(echo "$response" | tail -n1)
if [ "$http_code" = "400" ] || [ "$http_code" = "500" ]; then
  log_success "Status HTTP: $http_code ✓ (oczekiwany błąd)"
else
  log_error "Nieprawidłowy status HTTP: $http_code"
fi
echo "----------------------------------------"
echo

# Test 10: Bardzo długi URL
test_case "Bardzo długi URL" \
  '{"url": "https://example.com/very/very/very/long/path/with/many/segments/and/parameters?param1=value1&param2=value2&param3=value3&param4=value4&param5=value5&param6=value6"}' \
  "200"

# Sprawdzenie S3 bucket
log_info "Sprawdzanie zawartości S3 bucket..."
BUCKET_NAME=$(terraform output -raw s3_bucket_name 2>/dev/null)

if [ -n "$BUCKET_NAME" ]; then
  file_count=$(aws s3 ls s3://$BUCKET_NAME/qr_codes/ --recursive 2>/dev/null | wc -l || echo "0")
  log_success "S3 Bucket: $BUCKET_NAME"
  log_success "Liczba plików QR w bucket: $file_count"

  if [ "$file_count" -gt 0 ]; then
    log_info "Ostatnie 3 pliki:"
    aws s3 ls s3://$BUCKET_NAME/qr_codes/ --recursive | tail -3
  fi
else
  log_warning "Nie udało się pobrać nazwy S3 bucket"
fi

echo
echo "🏁 Wszystkie testy zakończone!"
echo "📊 Podsumowanie dostępne w logach powyżej"
echo
echo "💡 Porady:"
echo "• Sprawdź wygenerowane kody QR w przeglądarce"
echo "• Zeskanuj kody QR telefonem, aby sprawdzić czy działają"
echo "• Monitoruj logi Lambda w AWS CloudWatch w przypadku problemów"
