#!/bin/bash

# Make sure script errors are visible
set -e

echo "Running A* algorithm tests for transfers optimization..."

# Create output directory if it doesn't exist
mkdir -p outputs

# Test 1: Easy problem (close station) - Śliczna → Prudnicka
echo "Test 1: Easy problem - Śliczna to Prudnicka (transfers optimization)"
echo "Easy problem - close station (transfers optimization)" >outputs/astar-s-sliczna-prudnicka.txt
python run_astar.py --start "Śliczna" --end "Prudnicka" --method "s" --time "16:25:00" >>outputs/astar-s-sliczna-prudnicka.txt 2>&1
echo "Test 1 completed."

# Test 2: Medium problem (few transfers) - Śliczna → most Grunwaldzki
echo "Test 2: Medium problem - Śliczna to most Grunwaldzki (transfers optimization)"
echo "Medium problem - few transfers (transfers optimization)" >outputs/astar-s-sliczna-mostGrunwaldzki.txt
python run_astar.py --start "Śliczna" --end "most Grunwaldzki" --method "s" --time "08:50:00" >>outputs/astar-s-sliczna-mostGrunwaldzki.txt 2>&1
echo "Test 2 completed."

# Test 3: Hard problem (many transfers) - Śliczna → Bezpieczna
echo "Test 3: Hard problem - Śliczna to Bezpieczna (transfers optimization)"
echo "Hard problem - many transfers (transfers optimization)" >outputs/astar-s-sliczna-bezpieczna.txt
python run_astar.py --start "Śliczna" --end "Bezpieczna" --method "s" --time "16:25:00" >>outputs/astar-s-sliczna-bezpieczna.txt 2>&1
echo "Test 3 completed."

echo "All transfers optimization tests completed. Results saved in the outputs directory."
