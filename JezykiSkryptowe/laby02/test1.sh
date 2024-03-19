set -x

start=$(date +%s.%N)
parallel --pipepart -a data/Nasa python only_poland.py > output.txt
end=$(date +%s.%N)

echo "Execution time: "
echo "scale=3; $end - $start" | bc