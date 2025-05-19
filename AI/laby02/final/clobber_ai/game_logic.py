# clobber_project/clobber_ai/game_logic.py
import sys
import time
import math
from .board import Board
from .constants import BLACK  # Only need BLACK for starting player
from .heuristics import HEURISTICS_MAP
from .algorithms import find_best_move_minimax, find_best_move_alphabeta


def play_game(
    initial_board_str: str | None,
    rows: int,
    cols: int,
    p1_algo_choice: str,
    p1_heuristic_name: str,
    p1_depth: int,
    p2_algo_choice: str,
    p2_heuristic_name: str,
    p2_depth: int,
    # No need for testing_mode flag, the find_best_move functions now always return nodes
):
    # The `visited_nodes_count` global from constants is not used here directly for calculation.
    # The find_best_move functions return the count for their specific decision.

    game_board = Board(rows, cols, initial_board_str)
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
    stderr_log_entries = []  # To store (player, nodes_for_decision, time_for_decision)
    total_decision_making_time = 0.0
    game_round_num = 1

    while True:
        print(
            f"\n--- Round {game_round_num}, Player {current_player_char}'s turn ---",
            file=sys.stderr,
        )
        game_board.display(sys.stderr)
        possible_moves = game_board.get_possible_moves(current_player_char)

        if not possible_moves:
            print(f"Player {current_player_char} has no moves.", file=sys.stderr)
            opponent_char = game_board.get_opponent(current_player_char)
            if not game_board.get_possible_moves(opponent_char):
                print(
                    f"Opponent Player {opponent_char} also has no moves. Game Over.",
                    file=sys.stderr,
                )
                break
            else:
                print(f"Player {current_player_char} passes turn.", file=sys.stderr)
        else:
            print(f"Player {current_player_char} is thinking...", file=sys.stderr)
            sys.stderr.flush()

            start_time_move_decision = (
                time.perf_counter()
            )  # Use perf_counter for precision
            nodes_for_this_decision = 0  # Initialize

            if current_player_char == BLACK:
                best_move, nodes_for_this_decision = p1_find_move_func(
                    game_board, p1_depth, BLACK, p1_heuristic_func
                )
            else:  # WHITE's turn
                best_move, nodes_for_this_decision = p2_find_move_func(
                    game_board,
                    p2_depth,
                    current_player_char,
                    p2_heuristic_func,  # Pass WHITE explicitly
                )

            time_taken_move_decision = time.perf_counter() - start_time_move_decision
            total_decision_making_time += time_taken_move_decision

            stderr_log_entries.append(
                (current_player_char, nodes_for_this_decision, time_taken_move_decision)
            )

            if best_move is None:  # Should only happen if possible_moves was empty
                if possible_moves:  # Should not occur if AI is correct
                    sys.stderr.write(
                        f"Warning: Player {current_player_char} AI returned no move, picking first available.\n"
                    )
                    best_move = possible_moves[0]
                else:  # Truly no moves
                    print(
                        f"Player {current_player_char} confirmed no moves. Game might be over.",
                        file=sys.stderr,
                    )
                    break

            (from_r, from_c), (to_r, to_c) = best_move
            print(
                f"Player {current_player_char} chose move: ({from_r},{from_c}) -> ({to_r},{to_c})",
                file=sys.stderr,
            )
            game_board.make_move(best_move, current_player_char)
            last_successful_mover = current_player_char
            ply_count += 1

            # Check if game ends immediately after this move
            opponent_char = game_board.get_opponent(current_player_char)
            current_player_can_move_again = bool(
                game_board.get_possible_moves(current_player_char)
            )
            opponent_can_move = bool(game_board.get_possible_moves(opponent_char))

            if not current_player_can_move_again and not opponent_can_move:
                print(
                    f"Neither player can move after Player {current_player_char}'s move. Game Over.",
                    file=sys.stderr,
                )
                break

        current_player_char = game_board.get_opponent(current_player_char)
        if (
            current_player_char == BLACK
        ):  # New round starts when it's Black's turn again
            game_round_num += 1
        sys.stderr.flush()

    # --- Output Final Results ---
    print("\n====== FINAL BOARD STATE ======", file=sys.stdout)
    game_board.display(sys.stdout)

    winner_player = last_successful_mover
    num_rounds_played = math.ceil(ply_count / 2.0)

    sys.stdout.write(
        f"Rounds: {int(num_rounds_played)}, Winner: Player {winner_player if winner_player else 'None'}\n"
    )
    sys.stdout.flush()

    print("\n====== STATISTICS (stderr) ======", file=sys.stderr)
    total_visited_nodes_sum = 0
    for i, (player, nodes, t_decision) in enumerate(stderr_log_entries):
        sys.stderr.write(
            f"Decision {i + 1} by {player}: Visited nodes: {nodes}, Time: {t_decision:.4f}s\n"
        )
        total_visited_nodes_sum += nodes

    sys.stderr.write(
        f"Total visited nodes (sum over all decisions): {total_visited_nodes_sum}\n"
    )
    sys.stderr.write(
        f"Total algorithm decision-making time: {total_decision_making_time:.4f}s\n"
    )
    sys.stderr.flush()

    # Return game outcome for testing script if needed
    return {
        "winner": winner_player,
        "rounds": int(num_rounds_played),
        "ply_count": ply_count,
        "p1_total_nodes": sum(s[1] for s in stderr_log_entries if s[0] == BLACK),
        "p2_total_nodes": sum(
            s[1] for s in stderr_log_entries if s[0] != BLACK
        ),  # Assuming WHITE
        "p1_total_time_s": sum(s[2] for s in stderr_log_entries if s[0] == BLACK),
        "p2_total_time_s": sum(s[2] for s in stderr_log_entries if s[0] != BLACK),
    }
