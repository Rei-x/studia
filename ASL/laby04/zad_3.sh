#!/bin/bash

echo "Wprowadź pierwszą liczbę:"
read first_number
echo "Wprowadź drugą liczbę:"
read second_number

if [ $first_number -eq $second_number ]; then
    echo "Liczba $first_number i liczba $second_number są równe"
else
    echo "Liczba $first_number i liczba $second_number są różne"
fi