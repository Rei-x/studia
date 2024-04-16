#!/bin/bash

echo "Czy jest wieczór? (tak/nie)"
read -r answer

case "$answer" in
"tak")
    echo "Dobry wieczór"
    ;;
"nie")
    echo "Dzień dobry"
    ;;
*)
    echo "Nie rozpoznana odpowiedź: $answer"
    ;;
esac
