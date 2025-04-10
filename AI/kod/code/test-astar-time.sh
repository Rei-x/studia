#!/bin/bash

set -e

echo "Running A* algorithm tests for different scenarios..."

mkdir -p outputs

echo "Test 1: Easy problem - Śliczna to Prudnicka"
echo "Easy problem - close station" >outputs/sliczna-prudnicka.txt
python run_astar.py --start "Śliczna" --end "Prudnicka" --method "t" --time "16:25:00" >>outputs/sliczna-prudnicka.txt 2>&1
echo "Test 1 completed."

echo "Test 2: Medium problem - Śliczna to most Grunwaldzki"
echo "Medium problem - few transfers" >outputs/sliczna-mostGrunwaldzki.txt
python run_astar.py --start "Śliczna" --end "most Grunwaldzki" --method "t" --time "08:50:00" >>outputs/sliczna-mostGrunwaldzki.txt 2>&1
echo "Test 2 completed."

echo "Test 3: Hard problem - Śliczna to Bezpieczna"
echo "Hard problem - many transfers" >outputs/sliczna-bezpieczna.txt
python run_astar.py --start "Śliczna" --end "Bezpieczna" --method "t" --time "16:25:00" >>outputs/sliczna-bezpieczna.txt 2>&1
echo "Test 3 completed."

echo "All tests completed. Results saved in the outputs directory."
