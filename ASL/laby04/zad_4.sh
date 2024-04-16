#!/bin/bash

for file in "$@"; do
    if [ -e "$file" ]; then
        echo "Prawa dostępu do fileu $file: $(ls -l "$file" | cut -d ' ' -f 1)"
    else
        echo "Plik $file nie istnieje."
    fi
done
