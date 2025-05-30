# Generator kodów QR z AWS Lambda i S3

Ten projekt implementuje serwis do generowania kodów QR z URL-i przy użyciu AWS Lambda, S3 i Terraform.

## Architektura

- **AWS Lambda**: Funkcja do generowania kodów QR
- **S3 Bucket**: Przechowywanie wygenerowanych obrazów QR
- **Terraform**: Infrastruktura jako kod

## Wymagania

- Terraform >= 1.0
- AWS CLI skonfigurowane z odpowiednimi uprawnieniami
- **Konto edukacyjne AWS** z rolą LabRole
- Python 3.9+ (dla lokalnego testowania)
- pip3

## Konfiguracja dla konta edukacyjnego

Ten projekt jest skonfigurowany do pracy z kontami edukacyjnymi AWS Academy, które używają predefiniowanej roli `LabRole`. Nie musisz tworzyć dodatkowych ról IAM.

## Instalacja i uruchomienie

1. **Sklonuj repozytorium i przejdź do katalogu:**

   ```bash
   cd /home/rei/projects/studia/chmurki2/laby03
   ```

2. **Zainicjalizuj Terraform:**

   ```bash
   terraform init
   ```

3. **Sprawdź plan wdrożenia:**

   ```bash
   terraform plan
   ```

4. **Wdróż infrastrukturę:**

   ```bash
   terraform apply
   ```

5. **Po zakończeniu wdrożenia otrzymasz:**
   - URL funkcji Lambda
   - Nazwę S3 bucket
   - Publiczny URL S3 bucket

## Użycie

### Przez HTTP POST

Wyślij żądanie POST na URL funkcji Lambda:

```bash
curl -X POST "LAMBDA_FUNCTION_URL" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com"}'
```

### Przykładowa odpowiedź:

```json
{
  "success": true,
  "message": "Kod QR został wygenerowany pomyślnie",
  "original_url": "https://github.com",
  "qr_image_url": "https://qr-generator-bucket-unique-12345.s3.amazonaws.com/qr_codes/20250530_143022_abc123.png",
  "filename": "qr_codes/20250530_143022_abc123.png",
  "timestamp": "20250530_143022"
}
```

### Przykłady testów:

```bash
# Test z prostym URL
curl -X POST "LAMBDA_URL" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com"}'

# Test z URL bez protokołu
curl -X POST "LAMBDA_URL" \
  -H "Content-Type: application/json" \
  -d '{"url": "github.com"}'

# Test z długim URL
curl -X POST "LAMBDA_URL" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com/very/long/path/with/parameters?param1=value1&param2=value2"}'
```

## Funkcjonalności

- ✅ Generowanie kodów QR z URL-i
- ✅ Automatyczna walidacja i korekta URL-i
- ✅ Zapisywanie obrazów do S3 z publicznym dostępem
- ✅ Unikalne nazwy plików (timestamp + hash URL)
- ✅ Obsługa CORS
- ✅ Szczegółowe komunikaty błędów
- ✅ Organizacja plików w folderze `qr_codes/`

## Struktura plików

```
.
├── main.tf                    # Główna konfiguracja Terraform
├── build_lambda.sh           # Skrypt budowania pakietu Lambda
├── lambda_function/
│   ├── lambda_function.py    # Kod funkcji Lambda
│   └── requirements.txt      # Zależności Python
├── README.md                 # Ta dokumentacja
└── examples.md              # Przykłady użycia
```

## Koszty

- **Lambda**: ~$0.20 za milion żądań + czas wykonania
- **S3**: ~$0.023 za GB miesięcznie + żądania
- **Transfer danych**: Pierwsze GB miesięcznie bezpłatnie

## Bezpieczeństwo

- S3 bucket ma publiczny dostęp tylko do odczytu
- Lambda ma minimalne uprawnienia (tylko S3 PutObject)
- CORS skonfigurowany dla bezpiecznych żądań

## Czyszczenie zasobów

```bash
terraform destroy
```

## Troubleshooting

1. **Błąd uprawnień AWS**: Sprawdź konfigurację AWS CLI
2. **Błąd budowania Lambda**: Upewnij się, że masz pip3 i Python 3.9+
3. **Błąd nazwy bucket**: Zmień `bucket_name` w zmiennych Terraform na unikalną wartość
