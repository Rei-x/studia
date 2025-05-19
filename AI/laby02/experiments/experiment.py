import sys
import time
import math
import csv
import os


BLACK = "B"
WHITE = "W"
EMPTY = "_"


WIN_SCORE = 100000
LOSS_SCORE = -100000


visited_nodes_count = 0


class Board:
    def __init__(self, rows, cols, initial_board_str=None):
        self.rows = rows
        self.cols = cols
        if initial_board_str:
            self.grid = self._parse_board_str(initial_board_str)
        else:
            self.grid = self._default_clobber_setup()

    def _parse_board_str(self, board_str):
        grid = []
        lines = board_str.strip().split("\n")

        if not lines or not lines[0]:
            raise ValueError("Board string is empty or invalid.")

        if len(lines) != self.rows:
            raise ValueError(
                f"Board string has {len(lines)} rows, expected {self.rows}"
            )
        for r_idx, line in enumerate(lines):
            pieces = line.split()
            if len(pieces) != self.cols:
                raise ValueError(
                    f"Board string line {r_idx} has {len(pieces)} cols ({pieces}), expected {self.cols}"
                )
            grid.append(list(pieces))
        return grid

    def _default_clobber_setup(self):
        grid = [[EMPTY for _ in range(self.cols)] for _ in range(self.rows)]
        for r in range(self.rows):
            for c in range(self.cols):
                if (r % 2 == 0 and c % 2 == 0) or (r % 2 == 1 and c % 2 == 1):
                    grid[r][c] = BLACK
                else:
                    grid[r][c] = WHITE
        return grid

    def display(self, file=sys.stderr):
        for r in range(self.rows):
            file.write(" ".join(self.grid[r]) + "\n")
        file.flush()

    def get_opponent(self, player_char):
        return WHITE if player_char == BLACK else BLACK

    def is_valid_pos(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols

    def copy(self):
        new_board = Board(self.rows, self.cols)
        new_board.grid = [row[:] for row in self.grid]
        return new_board

    def get_possible_moves(self, player_char):
        moves = []
        opponent_char = self.get_opponent(player_char)
        for r_idx in range(self.rows):
            for c_idx in range(self.cols):
                if self.grid[r_idx][c_idx] == player_char:
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = r_idx + dr, c_idx + dc
                        if (
                            self.is_valid_pos(nr, nc)
                            and self.grid[nr][nc] == opponent_char
                        ):
                            moves.append(((r_idx, c_idx), (nr, nc)))
        return moves

    def make_move(self, move, player_char):
        (from_r, from_c), (to_r, to_c) = move
        self.grid[to_r][to_c] = player_char
        self.grid[from_r][from_c] = EMPTY


def h_piece_difference(board: Board, player_char_perspective: str):
    my_pieces = 0
    opponent_pieces = 0
    opponent_char = board.get_opponent(player_char_perspective)
    for r in range(board.rows):
        for c in range(board.cols):
            if board.grid[r][c] == player_char_perspective:
                my_pieces += 1
            elif board.grid[r][c] == opponent_char:
                opponent_pieces += 1
    return my_pieces - opponent_pieces


def h_mobility_difference(board: Board, player_char_perspective: str):
    my_moves_len = len(board.get_possible_moves(player_char_perspective))
    opponent_char = board.get_opponent(player_char_perspective)
    opponent_moves_len = len(board.get_possible_moves(opponent_char))
    return my_moves_len - opponent_moves_len


def h_combined_piece_mobility(board: Board, player_char_perspective: str):
    piece_weight = 1
    mobility_weight = 3
    score = 0
    score += piece_weight * h_piece_difference(board, player_char_perspective)
    score += mobility_weight * h_mobility_difference(board, player_char_perspective)
    return score


def h_adaptive_strategy(board: Board, player_char_perspective: str):
    my_pieces = 0
    opponent_pieces = 0
    opponent_char = board.get_opponent(player_char_perspective)

    for r_idx in range(board.rows):
        for c_idx in range(board.cols):
            if board.grid[r_idx][c_idx] == player_char_perspective:
                my_pieces += 1
            elif board.grid[r_idx][c_idx] == opponent_char:
                opponent_pieces += 1
    total_pieces_on_board = my_pieces + opponent_pieces

    my_mobility = len(board.get_possible_moves(player_char_perspective))
    opponent_mobility = len(board.get_possible_moves(opponent_char))
    total_mobility = my_mobility + opponent_mobility

    initial_total_pieces = board.rows * board.cols
    is_endgame = (total_pieces_on_board < initial_total_pieces * 0.45) or (
        total_mobility < (board.rows + board.cols) * 0.7
    )

    if is_endgame:
        return (
            h_mobility_difference(board, player_char_perspective) * 5
            + h_piece_difference(board, player_char_perspective) * 1
        )

    piece_diff_val = my_pieces - opponent_pieces

    if piece_diff_val < -1:
        return h_combined_piece_mobility(board, player_char_perspective)
    elif piece_diff_val > 1:
        return (
            h_piece_difference(board, player_char_perspective) * 2
            + h_mobility_difference(board, player_char_perspective) * 1
        )
    else:
        return h_combined_piece_mobility(board, player_char_perspective)


HEURISTICS_MAP = {
    "piece_diff": h_piece_difference,
    "mobility_diff": h_mobility_difference,
    "combined": h_combined_piece_mobility,
    "adaptive": h_adaptive_strategy,
}


def minimax_recursive(
    board: Board,
    depth: int,
    is_maximizing_player: bool,
    ai_player_char: str,
    heuristic_func,
    current_player_at_node: str,
):
    global visited_nodes_count
    visited_nodes_count += 1
    opponent_at_node = board.get_opponent(current_player_at_node)
    current_player_moves = board.get_possible_moves(current_player_at_node)

    if not current_player_moves:
        opponent_moves = board.get_possible_moves(opponent_at_node)
        if not opponent_moves:
            if opponent_at_node == ai_player_char:
                return WIN_SCORE
            return LOSS_SCORE
    if depth == 0:
        return heuristic_func(board, ai_player_char)
    if not current_player_moves:
        return minimax_recursive(
            board,
            depth - 1,
            not is_maximizing_player,
            ai_player_char,
            heuristic_func,
            opponent_at_node,
        )
    if is_maximizing_player:
        max_eval = -float("inf")
        for move in current_player_moves:
            new_board = board.copy()
            new_board.make_move(move, current_player_at_node)
            eval_score = minimax_recursive(
                new_board,
                depth - 1,
                False,
                ai_player_char,
                heuristic_func,
                opponent_at_node,
            )
            max_eval = max(max_eval, eval_score)
        return max_eval
    else:
        min_eval = float("inf")
        for move in current_player_moves:
            new_board = board.copy()
            new_board.make_move(move, current_player_at_node)
            eval_score = minimax_recursive(
                new_board,
                depth - 1,
                True,
                ai_player_char,
                heuristic_func,
                opponent_at_node,
            )
            min_eval = min(min_eval, eval_score)
        return min_eval


def find_best_move_minimax(
    board: Board, depth: int, ai_player_char: str, heuristic_func
):
    global visited_nodes_count
    visited_nodes_count = 0
    best_move = None
    max_eval = -float("inf")
    possible_moves = board.get_possible_moves(ai_player_char)
    if not possible_moves:
        return None, 0
    opponent_player_char = board.get_opponent(ai_player_char)

    for move in possible_moves:
        new_board = board.copy()
        new_board.make_move(move, ai_player_char)

        eval_score = minimax_recursive(
            new_board,
            depth - 1,
            False,
            ai_player_char,
            heuristic_func,
            opponent_player_char,
        )
        if eval_score > max_eval:
            max_eval = eval_score
            best_move = move
    return best_move, visited_nodes_count


def alphabeta_recursive(
    board: Board,
    depth: int,
    alpha: float,
    beta: float,
    is_maximizing_player: bool,
    ai_player_char: str,
    heuristic_func,
    current_player_at_node: str,
):
    global visited_nodes_count
    visited_nodes_count += 1
    opponent_at_node = board.get_opponent(current_player_at_node)
    current_player_moves = board.get_possible_moves(current_player_at_node)

    if not current_player_moves:
        opponent_moves = board.get_possible_moves(opponent_at_node)
        if not opponent_moves:
            if opponent_at_node == ai_player_char:
                return WIN_SCORE
            return LOSS_SCORE
    if depth == 0:
        return heuristic_func(board, ai_player_char)
    if not current_player_moves:
        return alphabeta_recursive(
            board,
            depth - 1,
            alpha,
            beta,
            not is_maximizing_player,
            ai_player_char,
            heuristic_func,
            opponent_at_node,
        )

    if is_maximizing_player:
        max_eval = -float("inf")

        for move in current_player_moves:
            new_board = board.copy()
            new_board.make_move(move, current_player_at_node)
            eval_score = alphabeta_recursive(
                new_board,
                depth - 1,
                alpha,
                beta,
                False,
                ai_player_char,
                heuristic_func,
                opponent_at_node,
            )
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float("inf")
        for move in current_player_moves:
            new_board = board.copy()
            new_board.make_move(move, current_player_at_node)
            eval_score = alphabeta_recursive(
                new_board,
                depth - 1,
                alpha,
                beta,
                True,
                ai_player_char,
                heuristic_func,
                opponent_at_node,
            )
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval


def find_best_move_alphabeta(
    board: Board, depth: int, ai_player_char: str, heuristic_func
):
    global visited_nodes_count
    visited_nodes_count = 0
    best_move = None
    max_eval = -float("inf")
    alpha = -float("inf")
    beta = float("inf")
    possible_moves = board.get_possible_moves(ai_player_char)
    if not possible_moves:
        return None, 0

    opponent_player_char = board.get_opponent(ai_player_char)

    for move in possible_moves:
        new_board = board.copy()
        new_board.make_move(move, ai_player_char)

        eval_score = alphabeta_recursive(
            new_board,
            depth - 1,
            alpha,
            beta,
            False,
            ai_player_char,
            heuristic_func,
            opponent_player_char,
        )
        if eval_score > max_eval:
            max_eval = eval_score
            best_move = move
        alpha = max(alpha, eval_score)
    return best_move, visited_nodes_count


def play_game_for_testing(
    initial_board_config: dict,
    p1_algo_choice: str,
    p1_heuristic_name: str,
    p1_depth: int,
    p2_algo_choice: str,
    p2_heuristic_name: str,
    p2_depth: int,
    verbose_curent_game=False,
):
    global visited_nodes_count

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

    game_move_stats = []

    game_round_num = 1

    while True:
        if verbose_curent_game:
            print(
                f"\n--- Test Game Round {game_round_num}, Player {current_player_char}'s turn ---",
                file=sys.stderr,
            )
            game_board.display(sys.stderr)

        possible_moves = game_board.get_possible_moves(current_player_char)

        if not possible_moves:
            if verbose_curent_game:
                print(f"Player {current_player_char} has no moves.", file=sys.stderr)
            opponent_char = game_board.get_opponent(current_player_char)
            opponent_moves = game_board.get_possible_moves(opponent_char)
            if not opponent_moves:
                if verbose_curent_game:
                    print(
                        f"Opponent Player {opponent_char} also has no moves. Game Over.",
                        file=sys.stderr,
                    )
                break
            else:
                if verbose_curent_game:
                    print(f"Player {current_player_char} passes turn.", file=sys.stderr)
        else:
            if verbose_curent_game:
                print(f"Player {current_player_char} is thinking...", file=sys.stderr)

            start_time_move_decision = time.perf_counter()

            nodes_for_this_decision = 0
            if current_player_char == BLACK:
                best_move, nodes_for_this_decision = p1_find_move_func(
                    game_board, p1_depth, BLACK, p1_heuristic_func
                )
            else:
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
                    if verbose_curent_game:
                        sys.stderr.write(
                            f"Warning: Test Player {current_player_char} AI returned no move, picking first available.\n"
                        )
                    best_move = possible_moves[0]
                else:
                    if verbose_curent_game:
                        print(
                            f"Player {current_player_char} confirmed no moves. Game might be over.",
                            file=sys.stderr,
                        )
                    break

            if verbose_curent_game:
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
                if verbose_curent_game:
                    print(
                        f"Neither player can move after Player {current_player_char}'s move. Game Over.",
                        file=sys.stderr,
                    )
                break

        current_player_char = game_board.get_opponent(current_player_char)
        if current_player_char == BLACK:
            game_round_num += 1
        if verbose_curent_game:
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
        "p2_heuristic": "combined",
        "p2_depth": 5,
        "p1_depths_to_test": [3, 4, 5],
        "scenarios": [],
    },
    {
        "id": "E3_Heuristic_Perf",
        "name": "Experiment 3: Heuristic Performance (P1 Heuristics vs P2 Fixed Combined)",
        "p1_algo": "alphabeta",
        "p2_algo": "alphabeta",
        "base_depth": 5,
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
        "base_depth": 5,
        "adaptive_heuristic": "adaptive",
        "other_heuristics": ["piece_diff", "mobility_diff", "combined"],
        "scenarios": [],
    },
    {
        "id": "E5_Asymmetric_Configs",
        "name": "Experiment 5: Asymmetric Configurations",
        "scenarios": [
            (("alphabeta", "combined", 3), ("alphabeta", "combined", 2)),
            (
                ("alphabeta", "adaptive", 2),
                ("minimax", "piece_diff", 2),
            ),
            (("alphabeta", "mobility_diff", 3), ("alphabeta", "piece_diff", 2)),
            (
                ("alphabeta", "adaptive", 3),
                ("alphabeta", "combined", 3),
            ),
        ],
    },
]


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


def run_all_experiments(output_csv_file="clobber_experiment_results.csv"):
    N_GAMES_PER_CONFIG = 2
    VERBOSE_CURRENT_GAME_PLAY = False

    file_exists = os.path.isfile(output_csv_file)
    csv_file = open(output_csv_file, "a", newline="")
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
            p1_depth = (
                exp_config.get(p1_d_template, p1_d_template)
                if isinstance(p1_d_template, str) and exp_config.get(p1_d_template)
                else p1_d_template
            )

            p2_heuristic = (
                exp_config.get(p2_h_template, p2_h_template)
                if isinstance(p2_h_template, str) and exp_config.get(p2_h_template)
                else p2_h_template
            )
            p2_depth = (
                exp_config.get(p2_d_template, p2_d_template)
                if isinstance(p2_d_template, str) and exp_config.get(p2_d_template)
                else p2_d_template
            )

            p1_depth = int(p1_depth)
            p2_depth = int(p2_depth)

            print(
                f"  Scenario {current_scenario_count}/{total_scenarios_to_run}: P1({p1_algo},{p1_heuristic},d{p1_depth}) vs P2({p2_algo},{p2_heuristic},d{p2_depth})"
            )

            p1_wins = 0
            p2_wins = 0
            draws_or_none = 0

            for game_num in range(1, N_GAMES_PER_CONFIG + 1):
                print(
                    f"    Game {game_num}/{N_GAMES_PER_CONFIG}...", end="", flush=True
                )
                start_game_time = time.time()

                game_results = play_game_for_testing(
                    INITIAL_BOARD_CONFIG,
                    p1_algo,
                    p1_heuristic,
                    p1_depth,
                    p2_algo,
                    p2_heuristic,
                    p2_depth,
                    verbose_curent_game=VERBOSE_CURRENT_GAME_PLAY,
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
                    game_results["winner"],
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

    csv_file.close()
    print("-" * 50)
    print(f"All experiments completed. Results saved to {output_csv_file}")


if __name__ == "__main__":
    run_all_experiments()
