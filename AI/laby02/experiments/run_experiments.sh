#!/bin/bash

# --- Configuration ---
PYTHON_SCRIPT="./v5.py" # Or "python3 ./clobber_ai.py" if not executable
OUTPUT_CSV="clobber_experiment_results.csv"
DEFAULT_BOARD_FILE="" # Optional: Path to a specific board file to use for all tests. Leave empty for default 5x6.

# Define parameter ranges for experiments
# You can customize these arrays for specific experiments
declare -a ALGORITHMS=("minimax" "alphabeta")
declare -a HEURISTICS=("piece_diff" "mobility_diff" "combined" "adaptive")
declare -a DEPTHS_P1=(2 3 4) # Depths for Player 1
declare -a DEPTHS_P2=(2 3)   # Depths for Player 2 (can be different for asymmetric tests)

# --- CSV Header ---
echo "GameID,P1_Algo,P1_Heuristic,P1_Depth,P2_Algo,P2_Heuristic,P2_Depth,BoardFile,Winner,Rounds,TotalNodesVisited,TotalGameTime_s" >"$OUTPUT_CSV"

GAME_ID_COUNTER=0

# --- Helper Function to Run a Single Game and Parse Results ---
run_game_and_parse() {
  local p1_algo=$1
  local p1_h=$2
  local p1_d=$3
  local p2_algo=$4
  local p2_h=$5
  local p2_d=$6
  local board_arg=""

  GAME_ID_COUNTER=$((GAME_ID_COUNTER + 1))

  echo "Running Game ID: $GAME_ID_COUNTER"
  echo "  P1: $p1_algo, $p1_h, depth $p1_d"
  echo "  P2: $p2_algo, $p2_h, depth $p2_d"
  if [ -n "$DEFAULT_BOARD_FILE" ]; then
    echo "  Board: $DEFAULT_BOARD_FILE"
    board_arg="--board_file $DEFAULT_BOARD_FILE"
  else
    echo "  Board: Default 5x6"
  fi

  # Construct the command
  # Capture both stdout and stderr
  # The Python script must not ask for interactive input if CLI args are given.
  # Ensure your Python script's argparse handles this (no --interactive_setup flag here).
  # Add 'stdbuf -oL -eL' if output seems overly buffered and parsing fails during long runs
  game_output=$(stdbuf -oL -eL $PYTHON_SCRIPT \
    --p1_algo "$p1_algo" --p1_heuristic "$p1_h" --p1_depth "$p1_d" \
    --p2_algo "$p2_algo" --p2_heuristic "$p2_h" --p2_depth "$p2_d" \
    $board_arg 2>&1) # Capture both stdout and stderr

  # --- Parse stdout for Winner and Rounds ---
  # Example stdout line: Rounds: 12, Winner: Player B
  winner_line=$(echo "$game_output" | grep -oP "Winner: Player \K([BWN])(?:one)?") # Extracts B, W, or N (from None)
  rounds_line=$(echo "$game_output" | grep -oP "Rounds: \K([0-9]+)")

  # Handle cases where parsing might fail (e.g., game crashes or output format changes)
  winner="${winner_line:-N/A}"
  # Correct winner extraction: if it's "Player B", just take B. If "None", take None.
  if [[ "$winner_line" == "Player B" ]]; then
    winner="B"
  elif [[ "$winner_line" == "Player W" ]]; then
    winner="W"
  elif [[ "$winner_line" == "None" ]]; then
    winner="None"
  else
    winner="N/A" # Fallback for unexpected format
  fi

  raw_winner_info=$(echo "$game_output" | grep "Winner:")
  if echo "$raw_winner_info" | grep -q "Player B"; then
    winner="B"
  elif echo "$raw_winner_info" | grep -q "Player W"; then
    winner="W"
  elif echo "$raw_winner_info" | grep -q "Winner: None"; then # Check for "Winner: None" explicitly
    winner="None"
  else
    winner="N/A" # Fallback
  fi

  rounds="${rounds_line:-0}"

  # --- Parse stderr for Total Nodes and Total Time ---
  # Example stderr lines:
  # Total visited nodes (sum over all decisions): 12345
  # Total algorithm decision-making time: 67.8901s
  total_nodes=$(echo "$game_output" | grep -oP "Total visited nodes \(sum over all decisions\): \K([0-9]+)")
  total_time_s=$(echo "$game_output" | grep -oP "Total algorithm decision-making time: \K([0-9]+\.?[0-9]*)")

  total_nodes="${total_nodes:-0}"
  total_time_s="${total_time_s:-0.0}"

  # --- Append to CSV ---
  echo "$GAME_ID_COUNTER,$p1_algo,$p1_h,$p1_d,$p2_algo,$p2_h,$p2_d,${DEFAULT_BOARD_FILE:-Default},$winner,$rounds,$total_nodes,$total_time_s" >>"$OUTPUT_CSV"
  echo "Result: Winner=$winner, Rounds=$rounds, Nodes=$total_nodes, Time=${total_time_s}s"
  echo "--------------------------------------------------"
  # Optional: add a small delay if needed, e.g., to avoid overwhelming system
  # sleep 0.1
}

# --- Experiment Scenarios ---

echo "Starting Clobber AI Experiments..."

# Experiment 1: Algorithm Comparison (Minimax vs. Alpha-Beta)
# Fix heuristic and depth, vary algorithms. Both players use same settings.
echo ">>> Experiment 1: Algorithm Comparison (Minimax vs. Alpha-Beta)"
fixed_h="combined"
fixed_d=2 # Choose a depth Minimax can handle in reasonable time
for algo in "${ALGORITHMS[@]}"; do
  run_game_and_parse "$algo" "$fixed_h" "$fixed_d" "$algo" "$fixed_h" "$fixed_d"
done
# Consider also Alpha-Beta at a slightly higher depth to show its advantage
# run_game_and_parse "alphabeta" "$fixed_h" 3 "alphabeta" "$fixed_h" 3

# Experiment 2: Impact of Search Depth for Player 1
# P1: Alpha-Beta, fixed good heuristic, varying depth
# P2: Alpha-Beta, fixed good heuristic, fixed moderate depth (baseline opponent)
echo ">>> Experiment 2: Impact of P1 Search Depth"
p1_h_depth_exp="adaptive" # Or "combined"
p2_algo_depth_exp="alphabeta"
p2_h_depth_exp="adaptive" # Or "combined"
p2_d_depth_exp=2          # Baseline P2 depth
for p1_d_val in "${DEPTHS_P1[@]}"; do
  # Ensure P1 uses alphabeta for this, as Minimax would be too slow at higher depths
  run_game_and_parse "alphabeta" "$p1_h_depth_exp" "$p1_d_val" \
    "$p2_algo_depth_exp" "$p2_h_depth_exp" "$p2_d_depth_exp"
done

# Experiment 3: Heuristic Performance Comparison for Player 1
# P1: Alpha-Beta, varying heuristics, fixed depth
# P2: Alpha-Beta, fixed strong heuristic (e.g., adaptive or combined), fixed depth
echo ">>> Experiment 3: Heuristic Performance Comparison for P1"
p1_algo_heur_exp="alphabeta"
p1_d_heur_exp=3
p2_algo_heur_exp="alphabeta"
p2_h_baseline="adaptive" # Baseline heuristic for P2
p2_d_heur_exp=3
for p1_h_val in "${HEURISTICS[@]}"; do
  run_game_and_parse "$p1_algo_heur_exp" "$p1_h_val" "$p1_d_heur_exp" \
    "$p2_algo_heur_exp" "$p2_h_baseline" "$p2_d_heur_exp"
done
# Optional: Round-robin where P1 heuristic plays P2 heuristic for all combinations
# This would be a nested loop for p1_h_val and another for p2_h_val

# Experiment 4: Asymmetric Configurations (Example)
# Pit different strategies/depths against each other
echo ">>> Experiment 4: Asymmetric Configurations"
# Example 1: Deeper P1 vs. Shallower P2 (same heuristic)
run_game_and_parse "alphabeta" "adaptive" 3 "alphabeta" "adaptive" 2
# Example 2: Different heuristics, same depth/algo
run_game_and_parse "alphabeta" "piece_diff" 3 "alphabeta" "mobility_diff" 3
# Example 3: Adaptive vs. Combined
run_game_and_parse "alphabeta" "adaptive" 3 "alphabeta" "combined" 3

# You can add more experiment blocks or a more exhaustive full factorial loop:
# echo ">>> Full Factorial (subset - CAUTION: can be very long)"
# for p1a in "alphabeta"; do # Focus on alphabeta for broader tests
#   for p1h in "${HEURISTICS[@]}"; do
#     for p1d in 2 3; do # Select a couple of depths
#       for p2a in "alphabeta"; do
#         for p2h in "${HEURISTICS[@]}"; do
#           for p2d in 2 3; do
#             # Optional: Add a condition to skip if P1 and P2 settings are identical and already run
#             # Or skip if P1 settings == P2 settings to avoid redundant symmetric games
#             # if [[ "$p1a" == "$p2a" && "$p1h" == "$p2h" && "$p1d" == "$p2d" ]]; then
#             #   if [ some_flag_to_indicate_symmetric_run_done ]; then continue; fi
#             # fi
#             run_game_and_parse "$p1a" "$p1h" "$p1d" "$p2a" "$p2h" "$p2d"
#           done
#         done
#       done
#     done
#   done
# done

echo "All experiments finished. Results saved to $OUTPUT_CSV"
