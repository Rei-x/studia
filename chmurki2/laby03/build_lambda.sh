#!/bin/bash

# Skrypt do budowania pakietu Lambda z zależnościami

set -e

echo "Budowanie pakietu Lambda..."

# Tworzenie katalogu tymczasowego
BUILD_DIR="lambda_build"
rm -rf $BUILD_DIR
mkdir $BUILD_DIR

# Kopiowanie kodu źródłowego
cp lambda_function/lambda_function.py $BUILD_DIR/
cp lambda_function/requirements.txt $BUILD_DIR/

# Przejście do katalogu budowania
cd $BUILD_DIR

# Instalacja zależności
pip3 install -r requirements.txt -t .

# Usunięcie niepotrzebnych plików
rm -rf *.dist-info
rm -rf __pycache__
rm requirements.txt

# Tworzenie archiwum ZIP
zip -r ../lambda_function.zip .

# Powrót do głównego katalogu
cd ..

# Usunięcie katalogu tymczasowego
rm -rf $BUILD_DIR

echo "Pakiet Lambda został utworzony: lambda_function.zip"
