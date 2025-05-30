# Przykłady użycia generatora kodów QR

## 1. Podstawowe testowanie

Po wdrożeniu infrastruktury otrzymasz URL funkcji Lambda. Użyj go w poniższych przykładach.

### Uzyskanie URL funkcji Lambda:

```bash
terraform output lambda_function_url
```

### Prosty test z curl:

```bash
# Zastąp LAMBDA_URL rzeczywistym URL z output Terraform
LAMBDA_URL="https://abc123xyz.lambda-url.us-east-1.on.aws/"

curl -X POST "$LAMBDA_URL" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com"}'
```

## 2. Różne scenariusze testowe

### Test z URL bez protokołu:

```bash
curl -X POST "$LAMBDA_URL" \
  -H "Content-Type: application/json" \
  -d '{"url": "www.google.com"}'
```

### Test z długim URL:

```bash
curl -X POST "$LAMBDA_URL" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://stackoverflow.com/questions/tagged/aws-lambda?tab=Votes&pagesize=50"}'
```

### Test z URL z parametrami:

```bash
curl -X POST "$LAMBDA_URL" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/search?q=terraform&type=code&sort=updated"}'
```

### Test z polskimi znakami w URL:

```bash
curl -X POST "$LAMBDA_URL" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://pl.wikipedia.org/wiki/Chmura_obliczeniowa"}'
```

## 3. Testy błędów

### Brak URL:

```bash
curl -X POST "$LAMBDA_URL" \
  -H "Content-Type: application/json" \
  -d '{}'
```

### Nieprawidłowy JSON:

```bash
curl -X POST "$LAMBDA_URL" \
  -H "Content-Type: application/json" \
  -d '{"url":'
```

### Pusty URL:

```bash
curl -X POST "$LAMBDA_URL" \
  -H "Content-Type: application/json" \
  -d '{"url": ""}'
```

## 4. Testowanie z poziomu przeglądarki (JavaScript)

```javascript
// Przykład użycia z JavaScript
const generateQR = async (url) => {
  const lambdaUrl = "YOUR_LAMBDA_URL_HERE";

  try {
    const response = await fetch(lambdaUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url: url }),
    });

    const result = await response.json();

    if (result.success) {
      console.log("QR kod wygenerowany:", result.qr_image_url);
      // Można teraz wyświetlić obraz QR
      const img = document.createElement("img");
      img.src = result.qr_image_url;
      document.body.appendChild(img);
    } else {
      console.error("Błąd:", result.error);
    }
  } catch (error) {
    console.error("Błąd sieci:", error);
  }
};

// Użycie
generateQR("https://github.com");
```

## 5. Testowanie z poziomu Python

```python
import requests
import json

def generate_qr_code(url, lambda_url):
    """Generuje kod QR dla podanego URL"""

    payload = {"url": url}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(lambda_url,
                               data=json.dumps(payload),
                               headers=headers)
        result = response.json()

        if response.status_code == 200 and result.get('success'):
            print(f"✅ Sukces! QR kod dostępny: {result['qr_image_url']}")
            return result['qr_image_url']
        else:
            print(f"❌ Błąd: {result.get('error', 'Nieznany błąd')}")
            return None

    except Exception as e:
        print(f"❌ Błąd połączenia: {e}")
        return None

# Przykład użycia
if __name__ == "__main__":
    lambda_url = "YOUR_LAMBDA_URL_HERE"

    test_urls = [
        "https://github.com",
        "www.google.com",
        "https://stackoverflow.com/questions/tagged/python",
        "invalid-url",
        ""
    ]

    for url in test_urls:
        print(f"\n🧪 Testowanie URL: {url}")
        generate_qr_code(url, lambda_url)
```

## 6. Sprawdzanie S3 Bucket

### Lista wygenerowanych plików:

```bash
# Pobierz nazwę bucket z Terraform
BUCKET_NAME=$(terraform output -raw s3_bucket_name)

# Wyświetl wszystkie pliki QR
aws s3 ls s3://$BUCKET_NAME/qr_codes/ --recursive
```

### Pobieranie pliku lokalnie:

```bash
# Pobierz konkretny plik QR
aws s3 cp s3://$BUCKET_NAME/qr_codes/filename.png ./downloaded_qr.png
```

## 7. Monitorowanie i logi

### Sprawdzenie logów Lambda:

```bash
# Pobierz nazwę funkcji
FUNCTION_NAME=$(terraform output -raw lambda_function_name)

# Sprawdź ostatnie logi
aws logs describe-log-groups --log-group-name-prefix "/aws/lambda/$FUNCTION_NAME"
```

## 8. Automatyczne testowanie

Skrypt do automatycznego testowania różnych scenariuszy:

```bash
#!/bin/bash

# test_qr_generator.sh
LAMBDA_URL=$(terraform output -raw lambda_function_url)

echo "🧪 Rozpoczynanie testów generatora QR..."

# Test 1: Prawidłowy URL
echo "Test 1: Prawidłowy URL"
curl -s -X POST "$LAMBDA_URL" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com"}' | jq '.'

echo -e "\n---\n"

# Test 2: URL bez protokołu
echo "Test 2: URL bez protokołu"
curl -s -X POST "$LAMBDA_URL" \
  -H "Content-Type: application/json" \
  -d '{"url": "google.com"}' | jq '.'

echo -e "\n---\n"

# Test 3: Błędny request (brak URL)
echo "Test 3: Brak URL"
curl -s -X POST "$LAMBDA_URL" \
  -H "Content-Type: application/json" \
  -d '{}' | jq '.'

echo -e "\n🏁 Testy zakończone"
```

## 9. Przykładowe odpowiedzi

### Sukces:

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

### Błąd - brak URL:

```json
{
  "error": "URL jest wymagany",
  "example": {
    "url": "https://example.com"
  }
}
```

### Błąd - nieprawidłowy URL:

```json
{
  "error": "Nieprawidłowy format URL"
}
```
