#!/bin/bash

# Make sure script errors are visible
set -e

echo "Running Dijkstra algorithm tests for different scenarios..."

# Create output directory if it doesn't exist
mkdir -p outputs

# Test 1: Easy problem (close station) - Śliczna → Prudnicka
echo "Test 1: Easy problem - Śliczna to Prudnicka"
echo "Easy problem - close station" >outputs/dijkstra-sliczna-prudnicka.txt
python run_dijkstra.py --start "Śliczna" --end "Prudnicka" --method "t" --time "16:25:00" >>outputs/dijkstra-sliczna-prudnicka.txt 2>&1
echo "Test 1 completed."

# Test 2: Medium problem (few transfers) - Śliczna → most Grunwaldzki
echo "Test 2: Medium problem - Śliczna to most Grunwaldzki"
echo "Medium problem - few transfers" >outputs/dijkstra-sliczna-mostGrunwaldzki.txt
python run_dijkstra.py --start "Śliczna" --end "most Grunwaldzki" --method "t" --time "08:50:00" >>outputs/dijkstra-sliczna-mostGrunwaldzki.txt 2>&1
echo "Test 2 completed."

# Test 3: Hard problem (many transfers) - Śliczna → Bezpieczna
echo "Test 3: Hard problem - Śliczna to Bezpieczna"
echo "Hard problem - many transfers" >outputs/dijkstra-sliczna-bezpieczna.txt
python run_dijkstra.py --start "Śliczna" --end "Bezpieczna" --method "t" --time "16:25:00" >>outputs/dijkstra-sliczna-bezpieczna.txt 2>&1
echo "Test 3 completed."

echo "All tests completed. Results saved in the outputs directory."
