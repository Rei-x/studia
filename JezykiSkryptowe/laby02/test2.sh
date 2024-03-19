start=$(date +%s.%N)
cat data/Nasa | python only_poland.py | python only_night_assets.py > output2.txt
end=$(date +%s.%N)

echo "Execution time: "
echo "scale=3; $end - $start" | bc