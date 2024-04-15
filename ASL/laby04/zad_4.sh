#!/bin/bash

for plik in "$@"; do
    if [ -e "$plik" ]; then
        echo "Prawa dostępu do pliku $plik: $(ls -l "$plik" | cut -d ' ' -f 1)"
    else
        echo "Plik $plik nie istnieje."
    fi
done