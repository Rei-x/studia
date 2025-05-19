import sys
import time
import math

# Constants for players and empty fields
BLACK = "B"
WHITE = "W"
EMPTY = "_"

# Scores for terminal states (win/loss) - large enough to dominate heuristics
WIN_SCORE = 100000
LOSS_SCORE = -100000

# Global counter for visited nodes (for statistics per decision)
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
        if len(lines) != self.rows:
            raise ValueError(
                f"Board string has {len(lines)} rows, expected {self.rows}"
            )
        for r_idx, line in enumerate(lines):
            pieces = line.split()
            if len(pieces) != self.cols:
                raise ValueError(
                    f"Board string line {r_idx} has {len(pieces)} cols, expected {self.cols}"
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

    def display(self, file=sys.stdout):
        for r in range(self.rows):
            file.write(" ".join(self.grid[r]) + "\n")

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


# --- Heuristics ---
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
    total_pieces = my_pieces + opponent_pieces

    my_mobility = len(board.get_possible_moves(player_char_perspective))
    opponent_mobility = len(board.get_possible_moves(opponent_char))
    total_mobility = my_mobility + opponent_mobility

    # Endgame definition (tunable parameters)
    # Consider endgame if total pieces are less than 40% of initial, or total mobility is low.
    is_endgame = (total_pieces < (board.rows * board.cols) * 0.4) or (
        total_mobility < (board.rows + board.cols) * 0.6
    )  # Lowered threshold for mobility based endgame

    if is_endgame:
        # sys.stderr.write(f"Adaptive (Player {player_char_perspective}): ENDGAME strategy\n")
        # In Clobber endgame, forcing opponent out of moves is critical.
        # Strongly prioritize mobility. Piece difference is secondary but can break ties.
        return (
            h_mobility_difference(board, player_char_perspective) * 5
            + h_piece_difference(board, player_char_perspective) * 1
        )

    # Midgame logic
    piece_diff_val = my_pieces - opponent_pieces

    if piece_diff_val < -1:  # Significantly behind in pieces
        # sys.stderr.write(f"Adaptive (Player {player_char_perspective}): BEHIND strategy\n")
        # Be more aggressive: h_combined_piece_mobility already weights mobility higher.
        return h_combined_piece_mobility(board, player_char_perspective)

    elif piece_diff_val > 1:  # Significantly ahead in pieces
        # sys.stderr.write(f"Adaptive (Player {player_char_perspective}): AHEAD strategy\n")
        # Play more conservatively: prioritize maintaining piece advantage, but don't get trapped.
        return (
            h_piece_difference(board, player_char_perspective) * 2
            + h_mobility_difference(board, player_char_perspective) * 1
        )

    else:  # Balanced game state
        # sys.stderr.write(f"Adaptive (Player {player_char_perspective}): BALANCED MIDGAME strategy\n")
        return h_combined_piece_mobility(board, player_char_perspective)


HEURISTICS_MAP = {
    "piece_diff": h_piece_difference,
    "mobility_diff": h_mobility_difference,
    "combined": h_combined_piece_mobility,
    "adaptive": h_adaptive_strategy,  # Added new adaptive heuristic
}


# --- Minimax Algorithm (unchanged from previous version) ---
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
        return None
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
    return best_move


# --- Alpha-Beta Pruning Algorithm (unchanged from previous version) ---
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
        return None
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
    return best_move


# --- Game Logic ---
def play_game(
    initial_board_str: str,
    rows: int,
    cols: int,
    p1_algo_choice: str,
    p1_heuristic_name: str,
    p1_depth: int,
    p2_algo_choice: str,
    p2_heuristic_name: str,
    p2_depth: int,
):  # Added P2 params
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

    stderr_log_entries = []
    start_time_total_game = time.time()

    while True:
        possible_moves = game_board.get_possible_moves(current_player_char)

        if not possible_moves:
            opponent_char = game_board.get_opponent(current_player_char)
            opponent_moves = game_board.get_possible_moves(opponent_char)
            if not opponent_moves:
                break
        else:
            start_time_move_decision = time.time()

            if current_player_char == BLACK:
                best_move = p1_find_move_func(
                    game_board, p1_depth, BLACK, p1_heuristic_func
                )
            else:
                best_move = p2_find_move_func(
                    game_board, p2_depth, WHITE, p2_heuristic_func
                )

            time_taken_move_decision = time.time() - start_time_move_decision
            nodes_for_this_move = visited_nodes_count

            stderr_log_entries.append(
                (current_player_char, nodes_for_this_move, time_taken_move_decision)
            )

            if best_move is None:
                # This case implies possible_moves was empty, which should be caught above.
                # Or AI failed to find a move despite options (should not happen if minimax/AB is correct)
                # If it does happen and there are moves, we can just pick one to prevent crash
                if possible_moves:
                    # sys.stderr.write(f"Warning: Player {current_player_char} AI returned no move, picking first available.\n")
                    best_move = possible_moves[0]
                else:  # Truly no moves, game should end.
                    break

            game_board.make_move(best_move, current_player_char)
            last_successful_mover = current_player_char
            ply_count += 1

            opponent_char = game_board.get_opponent(current_player_char)
            opponent_moves_after_current = game_board.get_possible_moves(opponent_char)
            if not opponent_moves_after_current:
                current_player_moves_after_own_move = game_board.get_possible_moves(
                    current_player_char
                )
                if not current_player_moves_after_own_move:
                    break  # Game ends, current_player_char (who just moved) wins

        current_player_char = game_board.get_opponent(current_player_char)

    total_game_time = time.time() - start_time_total_game

    game_board.display(sys.stdout)
    rounds = math.ceil(ply_count / 2.0)

    winner_player = last_successful_mover  # The one who made the last successful move
    if winner_player:
        sys.stdout.write(f"Rounds: {int(rounds)}, Winner: Player {winner_player}\n")
    else:
        sys.stdout.write(
            f"Rounds: {int(rounds)}, Winner: None (Game ended immediately or stalemate with no last mover)\n"
        )

    total_visited_nodes_sum = 0
    for i, (player, nodes, t_decision) in enumerate(stderr_log_entries):
        sys.stderr.write(
            f"Move {i + 1} by {player}: Visited nodes: {nodes}, Time: {t_decision:.4f}s\n"
        )
        total_visited_nodes_sum += nodes

    sys.stderr.write(
        f"Total visited nodes (sum over all moves): {total_visited_nodes_sum}\n"
    )
    sys.stderr.write(
        f"Total game algorithm time (decision making): {total_game_time:.4f}s\n"
    )


def get_player_settings(player_num_str: str, player_name: str):
    print(
        f"\n--- Settings for Player {player_num_str} ({player_name}) ---",
        file=sys.stderr,
    )

    chosen_heuristic_name = ""
    while chosen_heuristic_name not in HEURISTICS_MAP:
        prompt = f"Choose heuristic for Player {player_num_str} ({', '.join(HEURISTICS_MAP.keys())}): "
        chosen_heuristic_name = input(prompt).strip()
        if chosen_heuristic_name not in HEURISTICS_MAP:
            print(
                f"Invalid heuristic. Available: {', '.join(HEURISTICS_MAP.keys())}",
                file=sys.stderr,
            )

    search_depth = 0
    while search_depth <= 0:
        try:
            raw_depth = input(
                f"Enter max search depth (d) for Player {player_num_str} (e.g., 3): "
            ).strip()
            search_depth = int(raw_depth)
            if search_depth <= 0:
                print("Depth must be > 0.", file=sys.stderr)
        except ValueError:
            print("Invalid input for depth. Please enter an integer.", file=sys.stderr)
            search_depth = 0

    algo_choice = ""
    while algo_choice not in ["minimax", "alphabeta"]:
        algo_choice = (
            input(f"Choose algorithm for Player {player_num_str} (minimax/alphabeta): ")
            .strip()
            .lower()
        )
        if algo_choice not in ["minimax", "alphabeta"]:
            print(
                "Invalid algorithm choice. Type 'minimax' or 'alphabeta'.",
                file=sys.stderr,
            )

    return algo_choice, chosen_heuristic_name, search_depth


def main():
    default_rows, default_cols = 5, 6
    game_board_str = None
    rows, cols = default_rows, default_cols

    if not sys.stdin.isatty():
        raw_board_input = sys.stdin.read().strip()
        if raw_board_input:
            game_board_str = raw_board_input
            lines = game_board_str.split("\n")
            rows = len(lines)
            if rows > 0:
                cols = len(lines[0].split())
                print(f"Read board {rows}x{cols} from stdin.", file=sys.stderr)
            else:
                print(
                    "Empty board input from stdin, using default 5x6.", file=sys.stderr
                )
                rows, cols = default_rows, default_cols
                game_board_str = None  # Use default setup
        else:
            print("Empty stdin, using default 5x6 Clobber board.", file=sys.stderr)
    else:
        print(
            "No board piped via stdin, using default 5x6 Clobber board.",
            file=sys.stderr,
        )

    p1_algo, p1_heuristic, p1_depth = get_player_settings("1", "Black")
    p2_algo, p2_heuristic, p2_depth = get_player_settings("2", "White")

    print("\nStarting game with independent agent settings...", file=sys.stderr)

    play_game(
        initial_board_str=game_board_str,
        rows=rows,
        cols=cols,
        p1_algo_choice=p1_algo,
        p1_heuristic_name=p1_heuristic,
        p1_depth=p1_depth,
        p2_algo_choice=p2_algo,
        p2_heuristic_name=p2_heuristic,
        p2_depth=p2_depth,
    )


if __name__ == "__main__":
    main()
