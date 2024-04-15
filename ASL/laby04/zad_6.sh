#!/bin/bash

echo "Czy jest wieczór? (tak/nie)"
read odpowiedz

case "$odpowiedz" in
    "tak")
        echo "Dobry wieczór"
        ;;
    "nie")
        echo "Dzień dobry"
        ;;
    *)
        echo "Nie rozpoznana odpowiedź: $odpowiedz"
        ;;
esac