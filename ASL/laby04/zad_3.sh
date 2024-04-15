#!/bin/bash

echo "Wprowadź pierwszą liczbę:"
read liczba1
echo "Wprowadź drugą liczbę:"
read liczba2

if [ $liczba1 -eq $liczba2 ]; then
    echo "Liczba $liczba1 i liczba $liczba2 są równe"
else
    echo "Liczba $liczba1 i liczba $liczba2 są różne"
fi