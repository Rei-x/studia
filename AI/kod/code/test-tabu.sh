#!/bin/bash

set -e

echo "Running Tabu Search algorithm tests for time optimization..."

mkdir -p outputs

echo "Test 1: Easy problem - Śliczna, Prudnicka (time optimization)"
echo "Easy problem - close station (time optimization)" >outputs/tabu-t-sliczna-prudnicka.txt
python run_tabu.py --start "Śliczna" --stations "Prudnicka" --method "t" --time "16:25:00" >>outputs/tabu-t-sliczna-prudnicka.txt 2>&1
echo "Test 1 completed."

echo "Test 2: Medium problem - Śliczna, most Grunwaldzki, GALERIA DOMINIKAŃSKA (time optimization)"
echo "Medium problem - three stations (time optimization)" >outputs/tabu-t-sliczna-most-galeria.txt
python run_tabu.py --start "Śliczna" --stations "most Grunwaldzki,GALERIA DOMINIKAŃSKA" --method "t" --time "08:50:00" >>outputs/tabu-t-sliczna-most-galeria.txt 2>&1
echo "Test 2 completed."

echo "Test 3: Hard problem - Multiple stations (time optimization)"
echo "Hard problem - multiple stations (time optimization)" >outputs/tabu-t-multiple-stations.txt
python run_tabu.py --start "Śliczna" --stations "Bezpieczna,most Grunwaldzki,PL. GRUNWALDZKI,Ogród Botaniczny" --method "t" --time "16:25:00" --iterations 200 >>outputs/tabu-t-multiple-stations.txt 2>&1
echo "Test 3 completed."

echo "All Tabu Search time optimization tests completed. Results saved in the outputs directory."
