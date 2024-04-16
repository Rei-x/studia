#!/bin/bash

echo "Wprowadź pierwszą liczbę:"
read -r first_number
second_number=$1

echo "Suma została obliczona."
echo "$((first_number + second_number))"
