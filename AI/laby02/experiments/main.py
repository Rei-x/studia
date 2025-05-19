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
        # Standard Clobber: Black on (r+c)%2==0, White on (r+c)%2==1 if (0,0) is "black" field
        # Or simply alternating B W B W ...
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
        new_board = Board(
            self.rows, self.cols
        )  # Create with dummy dimensions initially
        new_board.grid = [row[:] for row in self.grid]
        return new_board

    def get_possible_moves(self, player_char):
        moves = []
        opponent_char = self.get_opponent(player_char)
        for r_idx in range(self.rows):
            for c_idx in range(self.cols):
                if self.grid[r_idx][c_idx] == player_char:
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:  # Orthogonal
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
# All heuristic functions take (board, player_char_perspective)
# and return a score from player_char_perspective's point of view.


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
    mobility_weight = 3  # Mobility is often more critical in Clobber

    score = 0
    score += piece_weight * h_piece_difference(board, player_char_perspective)
    score += mobility_weight * h_mobility_difference(board, player_char_perspective)
    return score


HEURISTICS_MAP = {
    "piece_diff": h_piece_difference,
    "mobility_diff": h_mobility_difference,
    "combined": h_combined_piece_mobility,
}


# --- Minimax Algorithm ---
def minimax_recursive(
    board: Board,
    depth: int,
    is_maximizing_player: bool,
    ai_player_char: str,  # The player for whom we are maximizing at the root
    heuristic_func,
    current_player_at_node: str,
):
    global visited_nodes_count
    visited_nodes_count += 1

    opponent_at_node = board.get_opponent(current_player_at_node)
    current_player_moves = board.get_possible_moves(current_player_at_node)

    # Terminal condition: Game Over (current player and opponent have no moves)
    if not current_player_moves:
        opponent_moves = board.get_possible_moves(opponent_at_node)
        if not opponent_moves:  # Game is truly over
            # The player who made the move TO THIS STATE wins.
            # That player is `opponent_at_node` (player from parent node).
            if opponent_at_node == ai_player_char:
                return WIN_SCORE
            return LOSS_SCORE

    if depth == 0:  # Depth limit reached
        return heuristic_func(board, ai_player_char)

    if not current_player_moves:  # Current player must pass (game not over yet)
        # Value is from opponent's perspective (recursive call with switched player)
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
                False,  # Minimizing player's turn
                ai_player_char,
                heuristic_func,
                opponent_at_node,
            )
            max_eval = max(max_eval, eval_score)
        return max_eval
    else:  # Minimizing player
        min_eval = float("inf")
        for move in current_player_moves:
            new_board = board.copy()
            new_board.make_move(move, current_player_at_node)
            eval_score = minimax_recursive(
                new_board,
                depth - 1,
                True,  # Maximizing player's turn
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
    visited_nodes_count = 0  # Reset for this top-level decision

    best_move = None
    max_eval = -float("inf")

    possible_moves = board.get_possible_moves(ai_player_char)
    if not possible_moves:
        return None

    opponent_player_char = board.get_opponent(ai_player_char)

    for move in possible_moves:
        new_board = board.copy()
        new_board.make_move(move, ai_player_char)
        # After AI's move, it's opponent's turn (minimizing)
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


# --- Alpha-Beta Pruning Algorithm ---
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

    if not current_player_moves:  # Current player must pass
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
        for (
            move
        ) in current_player_moves:  # Consider move ordering for better pruning later
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
    else:  # Minimizing player
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

    # Optional: Sort moves here to try potentially better moves first (improves pruning)
    # For example, sort by a shallow heuristic evaluation of the resulting state.
    # possible_moves.sort(key=lambda m: heuristic_func(board.copy().make_move(m, ai_player_char), ai_player_char), reverse=True)

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
        alpha = max(alpha, eval_score)  # Update alpha for root node as well
    return best_move


# --- Game Logic ---
def play_game(
    initial_board_str: str,
    rows: int,
    cols: int,
    p1_algo_choice: str,
    p1_heuristic_name: str,
    p1_depth: int,
    p2_is_optimal_ai: bool = True,
    p2_algo_choice: str = None,
    p2_heuristic_name: str = None,
    p2_depth: int = None,
):
    game_board = Board(rows, cols, initial_board_str)

    p1_heuristic_func = HEURISTICS_MAP[p1_heuristic_name]
    p1_find_move_func = (
        find_best_move_minimax
        if p1_algo_choice == "minimax"
        else find_best_move_alphabeta
    )

    if p2_is_optimal_ai:  # Basic version: P2 uses same settings as P1
        p2_algo_choice = p1_algo_choice
        p2_heuristic_name = p1_heuristic_name
        p2_depth = p1_depth

    p2_heuristic_func = HEURISTICS_MAP[p2_heuristic_name]
    p2_find_move_func = (
        find_best_move_minimax
        if p2_algo_choice == "minimax"
        else find_best_move_alphabeta
    )

    current_player_char = BLACK  # Black (Player 1) starts
    ply_count = 0
    last_successful_mover = None

    stderr_log_entries = []  # Store (visited_nodes, time_taken_move) tuples
    start_time_total_game = time.time()

    while True:
        possible_moves = game_board.get_possible_moves(current_player_char)

        if not possible_moves:
            opponent_char = game_board.get_opponent(current_player_char)
            opponent_moves = game_board.get_possible_moves(opponent_char)
            if not opponent_moves:  # Neither player can move: Game Over
                winner = last_successful_mover
                break
            # else: Current player passes turn, last_successful_mover doesn't change
        else:
            # Current player can move
            start_time_move_decision = time.time()
            nodes_for_this_move = 0  # will be updated by find_best_move via global

            if current_player_char == BLACK:  # P1's turn
                best_move = p1_find_move_func(
                    game_board, p1_depth, BLACK, p1_heuristic_func
                )
            else:  # P2's turn (WHITE)
                best_move = p2_find_move_func(
                    game_board, p2_depth, WHITE, p2_heuristic_func
                )

            time_taken_move_decision = time.time() - start_time_move_decision
            nodes_for_this_move = (
                visited_nodes_count  # Capture global count for this decision
            )

            stderr_log_entries.append((nodes_for_this_move, time_taken_move_decision))

            if (
                best_move is None
            ):  # Should only happen if possible_moves was empty, handled above
                print(
                    f"Error: Player {current_player_char} AI found no best move despite having options. This is unexpected.",
                    file=sys.stderr,
                )
                # Fallback if AI fails (should not happen with correct minimax/AB)
                if possible_moves:
                    best_move = possible_moves[0]
                else:
                    break  # Should have been caught

            game_board.make_move(best_move, current_player_char)
            last_successful_mover = current_player_char
            ply_count += 1

            # Check if opponent is now stuck (after current player's move)
            opponent_char = game_board.get_opponent(current_player_char)
            opponent_moves_after_current = game_board.get_possible_moves(opponent_char)
            if not opponent_moves_after_current:
                # If current player also has no moves now, game is over, current player wins
                current_player_moves_after_own_move = game_board.get_possible_moves(
                    current_player_char
                )
                if not current_player_moves_after_own_move:
                    winner = current_player_char
                    break
                # else: opponent is stuck, but current player can still move. Game continues, turn passes.
                # The game will end correctly in the next iterations.

        # Switch players for next turn
        current_player_char = game_board.get_opponent(current_player_char)

    total_game_time = time.time() - start_time_total_game

    # --- Output Results ---
    # Standard Output
    game_board.display(sys.stdout)
    rounds = math.ceil(ply_count / 2.0)  # A round is typically one move by each player

    if last_successful_mover:  # Winner is the one who made the last move
        sys.stdout.write(
            f"Rounds: {int(rounds)}, Winner: Player {last_successful_mover}\n"
        )
    else:  # Game ended before any move (e.g. 0x0 board)
        sys.stdout.write(
            f"Rounds: {int(rounds)}, Winner: None (Game ended immediately)\n"
        )

    # Standard Error Output
    total_visited_nodes_sum = 0
    player_for_log = BLACK
    for i, (nodes, t_decision) in enumerate(stderr_log_entries):
        sys.stderr.write(
            f"Move {i + 1} by {player_for_log}: Visited nodes: {nodes}, Time: {t_decision:.4f}s\n"
        )
        total_visited_nodes_sum += nodes
        player_for_log = WHITE if player_for_log == BLACK else BLACK

    sys.stderr.write(
        f"Total visited nodes (sum over all moves): {total_visited_nodes_sum}\n"
    )
    sys.stderr.write(f"Total game algorithm time: {total_game_time:.4f}s\n")


def main():
    default_rows, default_cols = 5, 6
    game_board_str = None
    rows, cols = default_rows, default_cols

    # Try to read board from stdin
    if not sys.stdin.isatty():  # Check if input is piped
        raw_board_input = sys.stdin.read().strip()
        if raw_board_input:
            game_board_str = raw_board_input
            lines = game_board_str.split("\n")
            rows = len(lines)
            if rows > 0:
                cols = len(lines[0].split())
            else:  # Should not happen with strip()
                print("Empty board input from stdin, using default.", file=sys.stderr)
                rows, cols = default_rows, default_cols
                game_board_str = None
            print(f"Read board {rows}x{cols} from stdin.", file=sys.stderr)
        else:
            print("Empty stdin, using default 5x6 Clobber board.", file=sys.stderr)
    else:
        print(
            "No board piped via stdin, using default 5x6 Clobber board.",
            file=sys.stderr,
        )

    print(
        "\nAvailable heuristics: " + ", ".join(HEURISTICS_MAP.keys()), file=sys.stderr
    )

    chosen_heuristic_name = ""
    while chosen_heuristic_name not in HEURISTICS_MAP:
        chosen_heuristic_name = input("Choose heuristic for Player 1 (Black): ").strip()
        if chosen_heuristic_name not in HEURISTICS_MAP:
            print(
                f"Invalid heuristic. Available: {', '.join(HEURISTICS_MAP.keys())}",
                file=sys.stderr,
            )

    search_depth_p1 = 0
    while search_depth_p1 <= 0:
        try:
            raw_depth = input(
                "Enter max search depth (d) for Player 1 (e.g., 3): "
            ).strip()
            search_depth_p1 = int(raw_depth)
            if search_depth_p1 <= 0:
                print("Depth must be > 0.", file=sys.stderr)
        except ValueError:
            print("Invalid input for depth. Please enter an integer.", file=sys.stderr)
            search_depth_p1 = 0

    algo_choice_p1 = ""
    while algo_choice_p1 not in ["minimax", "alphabeta"]:
        algo_choice_p1 = (
            input("Choose algorithm for Player 1 (minimax/alphabeta): ").strip().lower()
        )
        if algo_choice_p1 not in ["minimax", "alphabeta"]:
            print(
                "Invalid algorithm choice. Type 'minimax' or 'alphabeta'.",
                file=sys.stderr,
            )

    print(
        "\nStarting game. Basic version: Player 2 (White) will use same settings as Player 1.",
        file=sys.stderr,
    )

    play_game(
        initial_board_str=game_board_str,
        rows=rows,
        cols=cols,
        p1_algo_choice=algo_choice_p1,
        p1_heuristic_name=chosen_heuristic_name,
        p1_depth=search_depth_p1,
        p2_is_optimal_ai=True,
    )  # P2 mirrors P1 for basic version


if __name__ == "__main__":
    # To run:
    # 1. Save as clobber_ai.py
    # 2. Prepare a board file (e.g., board.txt):
    #    B W B W B
    #    W B W B W
    #    B W B W B
    #    W B W B W
    #    B W B W B
    #    W B W B W
    # 3. Run from terminal: `python clobber_ai.py < board.txt`
    #    Or for default board: `python clobber_ai.py`
    #    Then answer the prompts for heuristic, depth, and algorithm.
    main()
