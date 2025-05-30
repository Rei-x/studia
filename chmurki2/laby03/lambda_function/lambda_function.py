import json
import boto3
import qrcode
import io
import hashlib
import os
from datetime import datetime
from urllib.parse import urlparse

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    """
    Funkcja Lambda do generowania kodów QR z URL-i i zapisywania ich w S3
    """
    try:
        # Parsowanie danych wejściowych
        if 'body' in event:
            body = json.loads(event['body'])
        else:
            body = event
        
        url = body.get('url')
        if not url:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'URL jest wymagany',
                    'example': {'url': 'https://example.com'}
                })
            }
        
        # Walidacja URL
        try:
            parsed_url = urlparse(url)
            if not parsed_url.scheme:
                url = 'https://' + url
        except Exception:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'Nieprawidłowy format URL'
                })
            }
        
        # Generowanie kodu QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        # Tworzenie obrazu QR
        qr_image = qr.make_image(fill_color="black", back_color="white")
        
        # Konwersja obrazu do bytes
        img_buffer = io.BytesIO()
        qr_image.save(img_buffer)
        img_buffer.seek(0)
        
        # Generowanie unikalnej nazwy pliku
        url_hash = hashlib.md5(url.encode()).hexdigest()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"qr_codes/{timestamp}_{url_hash}.png"
        
        # Pobieranie nazwy bucket z zmiennych środowiskowych
        bucket_name = os.environ.get('BUCKET_NAME')
        if not bucket_name:
            raise Exception("BUCKET_NAME nie jest ustawiona w zmiennych środowiskowych")
        
        # Zapisywanie do S3
        s3_client.put_object(
            Bucket=bucket_name,
            Key=filename,
            Body=img_buffer.getvalue(),
            ContentType='image/png'
        )
        
        # Generowanie publicznego URL
        public_url = f"https://{bucket_name}.s3.amazonaws.com/{filename}"
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'success': True,
                'message': 'Kod QR został wygenerowany pomyślnie',
                'original_url': url,
                'qr_image_url': public_url,
                'filename': filename,
                'timestamp': timestamp
            })
        }
        
    except Exception as e:
        print(f"Błąd: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': f'Błąd wewnętrzny serwera: {str(e)}'
            })
        }
