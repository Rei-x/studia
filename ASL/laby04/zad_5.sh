#!/bin/bash

echo "Czy jest wieczór? (tak/nie)"
read odpowiedz

if [ "$odpowiedz" == "tak" ]; then
    echo "Dobry wieczór"
elif [ "$odpowiedz" == "nie" ]; then
    echo "Dzień dobry"
else
    echo "Nie rozpoznana odpowiedź: $odpowiedz"
fi