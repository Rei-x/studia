#!/bin/bash

echo "Wprowadź pierwszą liczbę:"
read -r first_number
echo "Wprowadź drugą liczbę:"
read -r second_number

if [ "$first_number" -eq "$second_number" ]; then
    echo "Liczba $first_number i liczba $second_number są równe"
else
    echo "Liczba $first_number i liczba $second_number są różne"
fi
