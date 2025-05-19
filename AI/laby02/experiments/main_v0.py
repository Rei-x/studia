import time
import sys

# Constants for players
PLAYER_B = "B"  # Black player (first player)
PLAYER_W = "W"  # White player (second player)
EMPTY = "_"


class ClobberGame:
    def __init__(self, board_str, current_player=PLAYER_B):
        self.board = self._parse_board(board_str)
        self.rows = len(self.board)
        self.cols = len(self.board[0])
        self.current_player = current_player

    def _parse_board(self, board_str):
        """Parses the input string into a 2D list representing the board."""
        return [list(row.split()) for row in board_str.strip().split("\n")]

    def __str__(self):
        """Returns a string representation of the board."""
        return "\n".join([" ".join(row) for row in self.board])

    def get_opponent(self, player):
        return PLAYER_W if player == PLAYER_B else PLAYER_B

    def get_possible_moves(self, player):
        """Generates all possible moves for the given player."""
        moves = []
        opponent = self.get_opponent(player)
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == player:
                    # Check orthogonal neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = r + dr, c + dc
                        if (
                            0 <= nr < self.rows
                            and 0 <= nc < self.cols
                            and self.board[nr][nc] == opponent
                        ):
                            moves.append(((r, c), (nr, nc)))
        return moves

    def make_move(self, move):
        """Applies a move to the board.
        move is a tuple of ((from_r, from_c), (to_r, to_c))
        Returns a new ClobberGame state.
        """
        (from_r, from_c), (to_r, to_c) = move
        new_board_list = [row[:] for row in self.board]  # Deep copy

        player_pawn = new_board_list[from_r][from_c]

        new_board_list[to_r][to_c] = player_pawn
        new_board_list[from_r][from_c] = EMPTY

        new_board_str = "\n".join([" ".join(row) for row in new_board_list])
        next_player = self.get_opponent(self.current_player)
        return ClobberGame(new_board_str, next_player)

    def is_game_over(self):
        """Checks if the game is over (no more moves for the current player)."""
        return not self.get_possible_moves(self.current_player)

    def get_winner(self, last_player_to_move):
        """Determines the winner. The player who made the last move wins."""
        # In Clobber, the player who makes the last move wins.
        # If is_game_over() is true, it means current_player has no moves.
        # So, the opponent of current_player made the last valid move.
        return last_player_to_move


# --- Heuristic Functions ---
def heuristic_piece_difference(game_state, player_to_evaluate_for):
    """Heuristic: Difference in piece count."""
    my_pieces = 0
    opponent_pieces = 0
    opponent = game_state.get_opponent(player_to_evaluate_for)
    for r in range(game_state.rows):
        for c in range(game_state.cols):
            if game_state.board[r][c] == player_to_evaluate_for:
                my_pieces += 1
            elif game_state.board[r][c] == opponent:
                opponent_pieces += 1
    return my_pieces - opponent_pieces


def heuristic_mobility_difference(game_state, player_to_evaluate_for):
    """Heuristic: Difference in the number of possible moves."""
    my_moves = len(game_state.get_possible_moves(player_to_evaluate_for))
    opponent_moves = len(
        game_state.get_possible_moves(game_state.get_opponent(player_to_evaluate_for))
    )
    return my_moves - opponent_moves


def heuristic_combined_score(game_state, player_to_evaluate_for):
    """Heuristic: A weighted combination of piece difference and mobility.
    Gives more weight to mobility.
    """
    piece_diff_weight = 1.0
    mobility_weight = 2.0  # Mobility is often more critical

    score = piece_diff_weight * heuristic_piece_difference(
        game_state, player_to_evaluate_for
    ) + mobility_weight * heuristic_mobility_difference(
        game_state, player_to_evaluate_for
    )
    return score


HEURISTICS = {
    "1": ("Piece Difference", heuristic_piece_difference),
    "2": ("Mobility Difference", heuristic_mobility_difference),
    "3": ("Combined Score (Mobility Weighted)", heuristic_combined_score),
}

# Global counter for visited nodes
VISITED_NODES = 0


# --- Minimax Algorithm ---
def minimax(
    game_state,
    depth,
    maximizing_player_is_ai_player,
    ai_player,
    chosen_heuristic_func,
    current_player_for_move,
):
    global VISITED_NODES
    VISITED_NODES += 1

    # Base cases
    if depth == 0 or game_state.is_game_over():
        # If game over, the player who *cannot* make a move loses.
        # The heuristic should evaluate from the perspective of the AI player whose best move we are trying to find.
        if game_state.is_game_over():
            # If current_player_for_move cannot move, their opponent (previous player) won.
            previous_player = game_state.get_opponent(current_player_for_move)
            if previous_player == ai_player:
                return float("inf"), None  # AI wins
            else:
                return float("-inf"), None  # AI loses
        return chosen_heuristic_func(game_state, ai_player), None

    possible_moves = game_state.get_possible_moves(current_player_for_move)
    if not possible_moves:  # Should be caught by is_game_over, but as a safeguard
        previous_player = game_state.get_opponent(current_player_for_move)
        if previous_player == ai_player:
            return float("inf"), None
        else:
            return float("-inf"), None

    best_move = None

    if (current_player_for_move == ai_player and maximizing_player_is_ai_player) or (
        current_player_for_move != ai_player and not maximizing_player_is_ai_player
    ):  # Maximizing player's turn
        max_eval = float("-inf")
        for move in possible_moves:
            new_game_state = game_state.make_move(move)
            evaluation, _ = minimax(
                new_game_state,
                depth - 1,
                maximizing_player_is_ai_player,
                ai_player,
                chosen_heuristic_func,
                new_game_state.current_player,
            )
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move
        return max_eval, best_move
    else:  # Minimizing player's turn
        min_eval = float("inf")
        for move in possible_moves:
            new_game_state = game_state.make_move(move)
            evaluation, _ = minimax(
                new_game_state,
                depth - 1,
                maximizing_player_is_ai_player,
                ai_player,
                chosen_heuristic_func,
                new_game_state.current_player,
            )
            if evaluation < min_eval:
                min_eval = evaluation
                best_move = move
        return min_eval, best_move


def get_best_move_minimax(game_state, depth, ai_player, chosen_heuristic_func):
    """Gets the best move for the AI player using Minimax."""
    # For Minimax, the top call is always for the AI player, who is trying to maximize their score.
    # The `maximizing_player_is_ai_player` flag helps the minimax function understand whose perspective to optimize for.
    # In a standard Minimax setup for finding the AI's best move, the AI is the maximizing player.
    _, best_move = minimax(
        game_state,
        depth,
        True,
        ai_player,
        chosen_heuristic_func,
        game_state.current_player,
    )
    return best_move


# --- Alpha-Beta Pruning Algorithm ---
def minimax_alphabeta(
    game_state,
    depth,
    alpha,
    beta,
    maximizing_player_is_ai_player,
    ai_player,
    chosen_heuristic_func,
    current_player_for_move,
):
    global VISITED_NODES
    VISITED_NODES += 1

    if depth == 0 or game_state.is_game_over():
        if game_state.is_game_over():
            previous_player = game_state.get_opponent(current_player_for_move)
            if previous_player == ai_player:
                return float("inf"), None
            else:
                return float("-inf"), None
        return chosen_heuristic_func(game_state, ai_player), None

    possible_moves = game_state.get_possible_moves(current_player_for_move)
    if not possible_moves:
        previous_player = game_state.get_opponent(current_player_for_move)
        if previous_player == ai_player:
            return float("inf"), None
        else:
            return float("-inf"), None

    best_move = None

    if (current_player_for_move == ai_player and maximizing_player_is_ai_player) or (
        current_player_for_move != ai_player and not maximizing_player_is_ai_player
    ):  # Maximizing player's turn (AI's perspective)
        max_eval = float("-inf")
        for move in possible_moves:
            new_game_state = game_state.make_move(move)
            evaluation, _ = minimax_alphabeta(
                new_game_state,
                depth - 1,
                alpha,
                beta,
                maximizing_player_is_ai_player,
                ai_player,
                chosen_heuristic_func,
                new_game_state.current_player,
            )
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break  # Beta cut-off
        return max_eval, best_move
    else:  # Minimizing player's turn (Opponent's perspective from AI's view)
        min_eval = float("inf")
        for move in possible_moves:
            new_game_state = game_state.make_move(move)
            evaluation, _ = minimax_alphabeta(
                new_game_state,
                depth - 1,
                alpha,
                beta,
                maximizing_player_is_ai_player,
                ai_player,
                chosen_heuristic_func,
                new_game_state.current_player,
            )
            if evaluation < min_eval:
                min_eval = evaluation
                best_move = move
            beta = min(beta, evaluation)
            if beta <= alpha:
                break  # Alpha cut-off
        return min_eval, best_move


def get_best_move_alphabeta(game_state, depth, ai_player, chosen_heuristic_func):
    """Gets the best move for the AI player using Minimax with Alpha-Beta pruning."""
    # The AI is the maximizing player from its own perspective.
    _, best_move = minimax_alphabeta(
        game_state,
        depth,
        float("-inf"),
        float("inf"),
        True,
        ai_player,
        chosen_heuristic_func,
        game_state.current_player,
    )
    return best_move


def main():
    global VISITED_NODES
    # Example usage:
    default_board_str = """B W B W B
W B W B W
B W B W B
W B W B W
B W B W B
W B W B W"""

    board_str = default_board_str  # Initialize with default

    # Allow user to input board, or use default
    print(
        "Enter initial board (m lines, n columns, B/W/_ separated by spaces), or press Enter for default 5x6 Clobber board:"
    )
    user_board_lines = []
    try:
        first_line = sys.stdin.readline().strip()
        if not first_line:
            print("Using default 5x6 Clobber board.")
            # board_str is already default_board_str
        else:
            user_board_lines.append(first_line)
            num_cols_ref = len(first_line.split())
            # Dynamically determine number of rows based on typical Clobber setup or user input structure
            # For simplicity, let's assume if user provides one line, they intend to provide all.
            # A more robust way would be to ask for dimensions or read until an empty line.
            # Reading (assumed) 5 more lines for a 6-row board if the first line was provided.
            # This part is tricky without knowing the exact intended number of rows from the user.
            # Let's make it more flexible: read lines until an empty line is entered.
            while True:
                line = sys.stdin.readline().strip()
                if not line:  # Stop if user provides an empty line (or EOF)
                    break
                if len(line.split()) != num_cols_ref:
                    print(
                        f"Inconsistent number of columns. Expected {num_cols_ref}. Got {len(line.split())}. Discarding custom input and using default board.",
                        file=sys.stderr,
                    )
                    board_str = default_board_str  # Revert to default
                    user_board_lines = []  # Clear partial input
                    break
                user_board_lines.append(line)

            if user_board_lines:  # If any lines were successfully read for custom board
                board_str = "\n".join(user_board_lines)

        # Validate board_str format (basic check)
        game_to_validate = ClobberGame(board_str)  # Try to create a game to validate
        print(f"Using board ({game_to_validate.rows}x{game_to_validate.cols}):")
        # print(game_to_validate) # Printing is done later with the main 'game' object
    except Exception as e:
        print(
            f"Error processing board input: {e}. Using default board.", file=sys.stderr
        )
        board_str = default_board_str  # Ensure default on any error
        # print("Using default 5x6 Clobber board.")
        # print(ClobberGame(board_str))

    game = ClobberGame(board_str, PLAYER_B)  # Black (Player 1) starts
    print("\nInitial board:")
    print(game)

    # Get heuristic choice and depth limit from user
    print("\nChoose a heuristic:")
    for key, (name, _) in HEURISTICS.items():
        print(f"{key}. {name}")

    chosen_heuristic_key = ""
    while chosen_heuristic_key not in HEURISTICS:
        chosen_heuristic_key = input(
            f"Enter heuristic number (1-{len(HEURISTICS)}): "
        ).strip()
        if chosen_heuristic_key not in HEURISTICS:
            print("Invalid choice. Please try again.")

    heuristic_name, chosen_heuristic_func = HEURISTICS[chosen_heuristic_key]
    print(f"Using heuristic: {heuristic_name}")

    depth_limit = 0
    while depth_limit <= 0:
        try:
            depth_limit = int(input("Enter maximum search depth (d > 0): ").strip())
            if depth_limit <= 0:
                print("Depth must be a positive integer.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

    print(f"Using search depth: {depth_limit}")

    # Ask user for algorithm choice
    print("\nChoose algorithm:")
    print("1. Minimax")
    print("2. Minimax with Alpha-Beta Pruning")
    algo_choice = ""
    while algo_choice not in ["1", "2"]:
        algo_choice = input("Enter algorithm choice (1 or 2): ").strip()
        if algo_choice not in ["1", "2"]:
            print("Invalid choice. Please enter 1 or 2.")

    use_alpha_beta = algo_choice == "2"
    if use_alpha_beta:
        print("Using Minimax with Alpha-Beta Pruning.")
    else:
        print("Using Minimax.")

    # Ask user if they want to play
    play_against_ai = (
        input("\nDo you want to play against the AI? (yes/no): ").strip().lower()
    )
    human_player = None
    if play_against_ai == "yes":
        while human_player not in [PLAYER_B, PLAYER_W]:
            human_player_choice = (
                input(
                    f"Do you want to be Player {PLAYER_B} (Black, goes first) or Player {PLAYER_W} (White)? Enter B or W: "
                )
                .strip()
                .upper()
            )
            if human_player_choice == PLAYER_B:
                human_player = PLAYER_B
            elif human_player_choice == PLAYER_W:
                human_player = PLAYER_W
            else:
                print("Invalid choice. Please enter B or W.")
        print(f"You are Player {human_player}.")

    # --- Game Loop (Basic Version) ---
    # Player 1 (AI, Black) vs Player 2 (Optimal, White)
    # Both use the same heuristic and depth for Player 2's "optimal" moves.

    rounds = 0
    game_start_time = time.time()  # Add time import

    current_game_state = game
    last_player_to_make_a_move = None

    while True:
        rounds += 1
        print(f"\n--- Round {rounds} ---")
        print(f"Current Player: {current_game_state.current_player}")
        print(current_game_state)

        if current_game_state.is_game_over():
            print("\nGame Over!")
            break

        VISITED_NODES = 0  # Reset for each move decision
        move_start_time = time.time()

        best_move_for_current_player = None

        if human_player and current_game_state.current_player == human_player:
            # Human player's turn
            possible_moves = current_game_state.get_possible_moves(human_player)
            if not possible_moves:
                print(f"Player {human_player} has no moves.")
                break
            print("Possible moves:")
            for i, move in enumerate(possible_moves):
                print(f"{i + 1}. {move}")

            chosen_move_idx = -1
            while chosen_move_idx < 0 or chosen_move_idx >= len(possible_moves):
                try:
                    move_choice = input(
                        f"Enter your move number (1-{len(possible_moves)}): "
                    ).strip()
                    chosen_move_idx = int(move_choice) - 1
                    if chosen_move_idx < 0 or chosen_move_idx >= len(possible_moves):
                        print("Invalid move number.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            best_move_for_current_player = possible_moves[chosen_move_idx]

        else:
            # AI player's turn
            ai_player_for_this_turn = (
                current_game_state.current_player
            )  # The player whose turn it is

            # In the basic version, both players play "optimally" using the chosen algorithm
            if use_alpha_beta:
                best_move_for_current_player = get_best_move_alphabeta(
                    current_game_state,
                    depth_limit,
                    ai_player_for_this_turn,
                    chosen_heuristic_func,
                )
            else:
                best_move_for_current_player = get_best_move_minimax(
                    current_game_state,
                    depth_limit,
                    ai_player_for_this_turn,
                    chosen_heuristic_func,
                )

        move_end_time = time.time()
        time_taken_for_move = move_end_time - move_start_time

        if best_move_for_current_player is None:
            # This should ideally be caught by is_game_over earlier,
            # but if minimax returns no move, it means no moves were possible.
            print(f"Player {current_game_state.current_player} has no moves.")
            break

        print(
            f"Player {current_game_state.current_player} chooses move: {best_move_for_current_player}"
        )
        print(
            f"(Nodes visited for this move: {VISITED_NODES}, Time: {time_taken_for_move:.4f}s)",
            file=sys.stderr,
        )

        last_player_to_make_a_move = current_game_state.current_player
        current_game_state = current_game_state.make_move(best_move_for_current_player)

    game_end_time = time.time()
    total_game_time = game_end_time - game_start_time

    # --- Output Results ---
    print("\nFinal Board:")
    print(
        current_game_state
    )  # This will be the board state where the current player has no moves

    winner = current_game_state.get_winner(
        last_player_to_make_a_move
    )  # The player who made the last move wins

    print(
        f"\nGame ended after {rounds - 1} full moves (or {rounds} states considered including initial)."
    )  # Or adjust round counting
    if winner:
        print(f"Player {winner} wins!")
    else:
        # This case should ideally not happen if last_player_to_make_a_move is tracked correctly
        # and game ends because one player cannot move.
        print("It's a draw or no moves were made after the start.")

    # Total nodes visited and total time are implicitly summed by stderr outputs per move.
    # For a total, you'd need to accumulate VISITED_NODES and time_taken_for_move globally if desired.
    print(
        f"Total algorithm execution time (sum of move calculations): {total_game_time:.4f}s (approx, includes print time etc.)",
        file=sys.stderr,
    )
    # A more accurate total node count would require accumulating VISITED_NODES across all get_best_move calls.


if __name__ == "__main__":
    main()
