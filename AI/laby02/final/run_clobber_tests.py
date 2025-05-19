# clobber_project/run_clobber_tests.py
import sys
import time
import math
import csv
import os

# Import from the clobber_ai package
from clobber_ai.board import Board
from clobber_ai.constants import (
    BLACK,
    WHITE,
)  # EMPTY, WIN_SCORE, LOSS_SCORE are used internally by modules
from clobber_ai.heuristics import HEURISTICS_MAP
from clobber_ai.algorithms import find_best_move_minimax, find_best_move_alphabeta
# Note: The game_logic.play_game is for interactive play with prints.
# For testing, we need a leaner version that just returns results.
# We'll adapt the core loop from the original play_game_for_testing directly here,
# using the now modularized components.


def play_game_for_testing_modular(
    initial_board_config: dict,
    p1_algo_choice: str,
    p1_heuristic_name: str,
    p1_depth: int,
    p2_algo_choice: str,
    p2_heuristic_name: str,
    p2_depth: int,
    verbose_current_game=False,
):
    game_board = Board(
        initial_board_config["rows"],
        initial_board_config["cols"],
        initial_board_config["board_str"],
    )

    p1_heuristic_func = HEURISTICS_MAP[p1_heuristic_name]
    p1_find_move_func = (
        find_best_move_minimax
        if p1_algo_choice == "minimax"
        else find_best_move_alphabeta
    )

    p2_heuristic_func = HEURISTICS_MAP[p2_heuristic_name]
    p2_find_move_func = (
        find_best_move_minimax
        if p2_algo_choice == "minimax"
        else find_best_move_alphabeta
    )

    current_player_char = BLACK
    ply_count = 0
    last_successful_mover = None

    game_move_stats = []  # List to store (player, nodes_for_decision, time_for_decision)
    game_round_num = 1

    while True:
        if verbose_current_game:
            print(
                f"\n--- Test Game Round {game_round_num}, Player {current_player_char}'s turn ---",
                file=sys.stderr,
            )
            game_board.display(sys.stderr)

        possible_moves = game_board.get_possible_moves(current_player_char)

        if not possible_moves:
            if verbose_current_game:
                print(f"Player {current_player_char} has no moves.", file=sys.stderr)
            opponent_char = game_board.get_opponent(current_player_char)
            opponent_moves = game_board.get_possible_moves(opponent_char)
            if not opponent_moves:
                if verbose_current_game:
                    print(
                        f"Opponent Player {opponent_char} also has no moves. Game Over.",
                        file=sys.stderr,
                    )
                break
            else:
                if verbose_current_game:
                    print(f"Player {current_player_char} passes turn.", file=sys.stderr)
        else:
            if verbose_current_game:
                print(f"Player {current_player_char} is thinking...", file=sys.stderr)

            start_time_move_decision = time.perf_counter()
            nodes_for_this_decision = 0
            best_move = None

            if current_player_char == BLACK:
                best_move, nodes_for_this_decision = p1_find_move_func(
                    game_board, p1_depth, BLACK, p1_heuristic_func
                )
            else:  # WHITE's turn
                best_move, nodes_for_this_decision = p2_find_move_func(
                    game_board, p2_depth, WHITE, p2_heuristic_func
                )

            time_taken_move_decision = time.perf_counter() - start_time_move_decision

            game_move_stats.append(
                {
                    "player": current_player_char,
                    "nodes": nodes_for_this_decision,
                    "time": time_taken_move_decision,
                }
            )

            if best_move is None:
                if possible_moves:
                    if verbose_current_game:
                        sys.stderr.write(
                            f"Warning: Test Player {current_player_char} AI returned no move, picking first available.\n"
                        )
                    best_move = possible_moves[0]
                else:
                    if verbose_current_game:
                        print(
                            f"Player {current_player_char} confirmed no moves. Game might be over.",
                            file=sys.stderr,
                        )
                    break

            if verbose_current_game:
                (from_r, from_c), (to_r, to_c) = best_move
                print(
                    f"Player {current_player_char} chose move: ({from_r},{from_c}) -> ({to_r},{to_c})",
                    file=sys.stderr,
                )

            game_board.make_move(best_move, current_player_char)
            last_successful_mover = current_player_char
            ply_count += 1

            opponent_char = game_board.get_opponent(current_player_char)
            current_player_can_move_again = bool(
                game_board.get_possible_moves(current_player_char)
            )
            opponent_can_move = bool(game_board.get_possible_moves(opponent_char))

            if not current_player_can_move_again and not opponent_can_move:
                if verbose_current_game:
                    print(
                        f"Neither player can move after Player {current_player_char}'s move. Game Over.",
                        file=sys.stderr,
                    )
                break

        current_player_char = game_board.get_opponent(current_player_char)
        if current_player_char == BLACK:
            game_round_num += 1
        if verbose_current_game:
            sys.stderr.flush()

    winner_player = last_successful_mover
    num_rounds_played = math.ceil(ply_count / 2.0)

    p1_total_nodes = sum(s["nodes"] for s in game_move_stats if s["player"] == BLACK)
    p2_total_nodes = sum(s["nodes"] for s in game_move_stats if s["player"] == WHITE)
    p1_total_time = sum(s["time"] for s in game_move_stats if s["player"] == BLACK)
    p2_total_time = sum(s["time"] for s in game_move_stats if s["player"] == WHITE)

    return {
        "winner": winner_player,
        "rounds": int(num_rounds_played),
        "ply_count": ply_count,
        "p1_total_nodes": p1_total_nodes,
        "p2_total_nodes": p2_total_nodes,
        "p1_total_time_s": p1_total_time,
        "p2_total_time_s": p2_total_time,
    }


# --- Experiment Definitions (can be kept largely the same) ---
DEFAULT_BOARD_ROWS = 5
DEFAULT_BOARD_COLS = 6
DEFAULT_BOARD_STR = None

INITIAL_BOARD_CONFIG = {
    "rows": DEFAULT_BOARD_ROWS,
    "cols": DEFAULT_BOARD_COLS,
    "board_str": DEFAULT_BOARD_STR,
}

EXPERIMENTS_SETUP = [
    {
        "id": "E1_Algo_Compare",
        "name": "Experiment 1: Algorithm Comparison (Minimax vs Alpha-Beta)",
        "base_heuristic": "combined",
        "base_depth": 2,
        "scenarios": [
            (
                ("minimax", "base_heuristic", "base_depth"),
                ("minimax", "base_heuristic", "base_depth"),
            ),
            (
                ("alphabeta", "base_heuristic", "base_depth"),
                ("alphabeta", "base_heuristic", "base_depth"),
            ),
            (
                ("minimax", "base_heuristic", "base_depth"),
                ("alphabeta", "base_heuristic", "base_depth"),
            ),
            (
                ("alphabeta", "base_heuristic", "base_depth"),
                ("minimax", "base_heuristic", "base_depth"),
            ),
        ],
    },
    {
        "id": "E2_Depth_Impact",
        "name": "Experiment 2: Impact of Search Depth (P1 AlphaBeta vs P2 Fixed)",
        "p1_algo": "alphabeta",
        "p1_base_heuristic": "combined",
        "p2_algo": "alphabeta",
        "p2_heuristic": "combined",  # This was 'combined' in your CSV
        "p2_depth": 5,  # This was 5 in your CSV for P2
        "p1_depths_to_test": [3, 4, 5],  # Matching your CSV data
        "scenarios": [],
    },
    {
        "id": "E3_Heuristic_Perf",
        "name": "Experiment 3: Heuristic Performance (P1 Heuristics vs P2 Fixed Combined)",
        "p1_algo": "alphabeta",
        "p2_algo": "alphabeta",
        "base_depth": 5,  # This was 5 in your CSV
        "p2_heuristic": "combined",
        "p1_heuristics_to_test": [
            "piece_diff",
            "mobility_diff",
            "combined",
            "adaptive",
        ],
        "scenarios": [],
    },
    {
        "id": "E4_Adaptive_Deep_Dive",
        "name": "Experiment 4: Adaptive Heuristic Deep Dive",
        "base_algo": "alphabeta",
        "base_depth": 5,  # This was 5 in your CSV
        "adaptive_heuristic": "adaptive",
        "other_heuristics": ["piece_diff", "mobility_diff", "combined"],
        "scenarios": [],
    },
    {
        "id": "E5_Asymmetric_Configs",
        "name": "Experiment 5: Asymmetric Configurations",
        "scenarios": [  # Adjusted to more closely match your CSV if possible
            (("alphabeta", "combined", 3), ("alphabeta", "combined", 2)),
            (("alphabeta", "adaptive", 2), ("minimax", "piece_diff", 2)),
            (("alphabeta", "mobility_diff", 3), ("alphabeta", "piece_diff", 2)),
            (("alphabeta", "adaptive", 3), ("alphabeta", "combined", 3)),
        ],
    },
]
# Populate scenarios for dynamic experiments (same logic as before)
for exp_setup in EXPERIMENTS_SETUP:
    if exp_setup["id"] == "E2_Depth_Impact":
        for p1_depth in exp_setup["p1_depths_to_test"]:
            p1_config = (exp_setup["p1_algo"], exp_setup["p1_base_heuristic"], p1_depth)
            p2_config = (
                exp_setup["p2_algo"],
                exp_setup["p2_heuristic"],
                exp_setup["p2_depth"],
            )
            exp_setup["scenarios"].append((p1_config, p2_config))
    elif exp_setup["id"] == "E3_Heuristic_Perf":
        for p1_h in exp_setup["p1_heuristics_to_test"]:
            p1_config = (exp_setup["p1_algo"], p1_h, exp_setup["base_depth"])
            p2_config = (
                exp_setup["p2_algo"],
                exp_setup["p2_heuristic"],
                exp_setup["base_depth"],
            )
            exp_setup["scenarios"].append((p1_config, p2_config))
    elif exp_setup["id"] == "E4_Adaptive_Deep_Dive":
        for other_h in exp_setup["other_heuristics"]:
            p1_config_adaptive = (
                exp_setup["base_algo"],
                exp_setup["adaptive_heuristic"],
                exp_setup["base_depth"],
            )
            p2_config_other = (exp_setup["base_algo"], other_h, exp_setup["base_depth"])
            exp_setup["scenarios"].append((p1_config_adaptive, p2_config_other))
            p1_config_other = (exp_setup["base_algo"], other_h, exp_setup["base_depth"])
            p2_config_adaptive = (
                exp_setup["base_algo"],
                exp_setup["adaptive_heuristic"],
                exp_setup["base_depth"],
            )
            exp_setup["scenarios"].append((p1_config_other, p2_config_adaptive))
        p_adaptive_config = (
            exp_setup["base_algo"],
            exp_setup["adaptive_heuristic"],
            exp_setup["base_depth"],
        )
        exp_setup["scenarios"].append((p_adaptive_config, p_adaptive_config))


def run_all_experiments(output_csv_file="clobber_experiment_results_modular.csv"):
    N_GAMES_PER_CONFIG = 2
    VERBOSE_CURRENT_GAME_PLAY = False

    file_exists = os.path.isfile(output_csv_file)
    # Ensure the directory for the output file exists if it's nested
    os.makedirs(os.path.dirname(output_csv_file) or ".", exist_ok=True)

    with open(output_csv_file, "a", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)

        if not file_exists or os.path.getsize(output_csv_file) == 0:
            header = [
                "ExperimentID",
                "ExperimentName",
                "GameNum",
                "P1_Algo",
                "P1_Heuristic",
                "P1_Depth",
                "P2_Algo",
                "P2_Heuristic",
                "P2_Depth",
                "Winner",
                "Rounds",
                "PlyCount",
                "P1_TotalNodes",
                "P2_TotalNodes",
                "P1_TotalTime_s",
                "P2_TotalTime_s",
            ]
            csv_writer.writerow(header)
        csv_file.flush()

        total_scenarios_to_run = sum(len(exp["scenarios"]) for exp in EXPERIMENTS_SETUP)
        print(
            f"Starting Clobber AI Experiments. Total unique scenarios: {total_scenarios_to_run}. Games per scenario: {N_GAMES_PER_CONFIG}."
        )
        print(f"Results will be saved to: {output_csv_file}")
        print("-" * 50)

        current_scenario_count = 0
        for exp_config in EXPERIMENTS_SETUP:
            exp_id = exp_config["id"]
            exp_name = exp_config["name"]
            print(f"\nRunning Experiment: {exp_name} (ID: {exp_id})")

            for p1_setup, p2_setup in exp_config["scenarios"]:
                current_scenario_count += 1
                p1_algo, p1_h_template, p1_d_template = p1_setup
                p2_algo, p2_h_template, p2_d_template = p2_setup

                p1_heuristic = (
                    exp_config.get(p1_h_template, p1_h_template)
                    if isinstance(p1_h_template, str) and exp_config.get(p1_h_template)
                    else p1_h_template
                )
                p1_depth_val = (
                    exp_config.get(p1_d_template, p1_d_template)
                    if isinstance(p1_d_template, str) and exp_config.get(p1_d_template)
                    else p1_d_template
                )
                p1_depth = int(p1_depth_val)

                p2_heuristic = (
                    exp_config.get(p2_h_template, p2_h_template)
                    if isinstance(p2_h_template, str) and exp_config.get(p2_h_template)
                    else p2_h_template
                )
                p2_depth_val = (
                    exp_config.get(p2_d_template, p2_d_template)
                    if isinstance(p2_d_template, str) and exp_config.get(p2_d_template)
                    else p2_d_template
                )
                p2_depth = int(p2_depth_val)

                print(
                    f"  Scenario {current_scenario_count}/{total_scenarios_to_run}: P1({p1_algo},{p1_heuristic},d{p1_depth}) vs P2({p2_algo},{p2_heuristic},d{p2_depth})"
                )

                p1_wins = 0
                p2_wins = 0
                draws_or_none = 0

                for game_num in range(1, N_GAMES_PER_CONFIG + 1):
                    print(
                        f"    Game {game_num}/{N_GAMES_PER_CONFIG}...",
                        end="",
                        flush=True,
                    )
                    start_game_time = time.time()

                    # Use the new modular play_game_for_testing_modular
                    game_results = play_game_for_testing_modular(
                        INITIAL_BOARD_CONFIG,
                        p1_algo,
                        p1_heuristic,
                        p1_depth,
                        p2_algo,
                        p2_heuristic,
                        p2_depth,
                        verbose_current_game=VERBOSE_CURRENT_GAME_PLAY,
                    )

                    end_game_time = time.time()
                    print(
                        f" done in {end_game_time - start_game_time:.2f}s. Winner: {game_results['winner']}",
                        flush=True,
                    )

                    if game_results["winner"] == BLACK:
                        p1_wins += 1
                    elif game_results["winner"] == WHITE:
                        p2_wins += 1
                    else:
                        draws_or_none += 1

                    row_data = [
                        exp_id,
                        exp_name,
                        game_num,
                        p1_algo,
                        p1_heuristic,
                        p1_depth,
                        p2_algo,
                        p2_heuristic,
                        p2_depth,
                        game_results["winner"]
                        if game_results["winner"]
                        else "None",  # Handle None winner for CSV
                        game_results["rounds"],
                        game_results["ply_count"],
                        game_results["p1_total_nodes"],
                        game_results["p2_total_nodes"],
                        f"{game_results['p1_total_time_s']:.4f}",
                        f"{game_results['p2_total_time_s']:.4f}",
                    ]
                    csv_writer.writerow(row_data)
                    csv_file.flush()

                print(
                    f"    Scenario Result (over {N_GAMES_PER_CONFIG} games): P1 Wins: {p1_wins}, P2 Wins: {p2_wins}, None/Other: {draws_or_none}"
                )

    print("-" * 50)
    print(f"All experiments completed. Results saved to {output_csv_file}")


if __name__ == "__main__":
    # To run this script, ensure you are in the 'clobber_project' directory
    # and run: python run_clobber_tests.py
    # The script assumes the 'clobber_ai' package is in the same directory or accessible via PYTHONPATH.
    # For direct execution, if clobber_ai is a subdirectory, Python should handle the imports.
    run_all_experiments()
