#!/bin/bash

echo "Czy jest wieczór? (tak/nie)"
read answer

if [ "$answer" == "tak" ]; then
    echo "Dobry wieczór"
elif [ "$answer" == "nie" ]; then
    echo "Dzień dobry"
else
    echo "Nie rozpoznana odpowiedź: $answer"
fi