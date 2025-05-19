# clobber_project/clobber_ai/algorithms.py
from .board import Board
from .constants import WIN_SCORE, LOSS_SCORE
# We will manage visited_nodes_count locally within these functions
# or pass it around if necessary, rather than relying on a global from constants.py for modules.
# For the test script, find_best_move_... functions will return node counts.
# For interactive play, we can use a global within this module if needed or make it an attribute of an AIPlayer class.

# For this refactoring, let's assume find_best_move functions will return (move, nodes_visited)
# and the recursive functions will update a passed-in counter object or a list.


class NodeCounter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

    def reset(self):
        self.count = 0

    def get_count(self):
        return self.count


def minimax_recursive(
    board: Board,
    depth: int,
    is_maximizing_player: bool,
    ai_player_char: str,
    heuristic_func,
    current_player_at_node: str,
    counter: NodeCounter,  # Pass counter
):
    counter.increment()
    opponent_at_node = board.get_opponent(current_player_at_node)
    current_player_moves = board.get_possible_moves(current_player_at_node)
    if not current_player_moves:
        opponent_moves = board.get_possible_moves(opponent_at_node)
        if not opponent_moves:
            return WIN_SCORE if opponent_at_node == ai_player_char else LOSS_SCORE
    if depth == 0:
        return heuristic_func(board, ai_player_char)
    if not current_player_moves:  # Current player must pass
        return minimax_recursive(
            board,
            depth - 1,
            not is_maximizing_player,
            ai_player_char,
            heuristic_func,
            opponent_at_node,
            counter,
        )
    if is_maximizing_player:
        max_eval = -float("inf")
        for move in current_player_moves:
            new_board = board.copy()
            new_board.make_move(move, current_player_at_node)
            max_eval = max(
                max_eval,
                minimax_recursive(
                    new_board,
                    depth - 1,
                    False,  # Minimizing player's turn
                    ai_player_char,
                    heuristic_func,
                    opponent_at_node,
                    counter,
                ),
            )
        return max_eval
    else:  # Minimizing player
        min_eval = float("inf")
        for move in current_player_moves:
            new_board = board.copy()
            new_board.make_move(move, current_player_at_node)
            min_eval = min(
                min_eval,
                minimax_recursive(
                    new_board,
                    depth - 1,
                    True,  # Maximizing player's turn
                    ai_player_char,
                    heuristic_func,
                    opponent_at_node,
                    counter,
                ),
            )
        return min_eval


def find_best_move_minimax(
    board: Board, depth: int, ai_player_char: str, heuristic_func
):
    node_counter = NodeCounter()  # Each call to find_best_move gets a fresh counter
    best_move = None
    max_eval = -float("inf")
    possible_moves = board.get_possible_moves(ai_player_char)
    if not possible_moves:
        return (
            None,
            node_counter.get_count(),
        )  # No moves, 0 nodes from this decision logic

    opponent_player_char = board.get_opponent(ai_player_char)
    for move in possible_moves:
        new_board = board.copy()
        new_board.make_move(move, ai_player_char)
        eval_score = minimax_recursive(
            new_board,
            depth - 1,
            False,  # Opponent's turn (minimizing)
            ai_player_char,
            heuristic_func,
            opponent_player_char,
            node_counter,  # Pass the counter
        )
        if eval_score > max_eval:
            max_eval = eval_score
            best_move = move
    return best_move, node_counter.get_count()


def alphabeta_recursive(
    board: Board,
    depth: int,
    alpha: float,
    beta: float,
    is_maximizing_player: bool,
    ai_player_char: str,
    heuristic_func,
    current_player_at_node: str,
    counter: NodeCounter,  # Pass counter
):
    counter.increment()
    opponent_at_node = board.get_opponent(current_player_at_node)
    current_player_moves = board.get_possible_moves(current_player_at_node)
    if not current_player_moves:
        opponent_moves = board.get_possible_moves(opponent_at_node)
        if not opponent_moves:
            return WIN_SCORE if opponent_at_node == ai_player_char else LOSS_SCORE
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
            counter,
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
                False,  # Minimizing player's turn
                ai_player_char,
                heuristic_func,
                opponent_at_node,
                counter,
            )
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha:  # Pruning condition
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
                True,  # Maximizing player's turn
                ai_player_char,
                heuristic_func,
                opponent_at_node,
                counter,
            )
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha:  # Pruning condition
                break
        return min_eval


def find_best_move_alphabeta(
    board: Board, depth: int, ai_player_char: str, heuristic_func
):
    node_counter = NodeCounter()  # Fresh counter for this decision
    best_move = None
    max_eval = -float("inf")
    alpha = -float("inf")
    beta = float("inf")
    possible_moves = board.get_possible_moves(ai_player_char)
    if not possible_moves:
        return None, node_counter.get_count()

    opponent_player_char = board.get_opponent(ai_player_char)
    for move in possible_moves:
        new_board = board.copy()
        new_board.make_move(move, ai_player_char)
        eval_score = alphabeta_recursive(
            new_board,
            depth - 1,
            alpha,
            beta,
            False,  # Opponent's turn (minimizing)
            ai_player_char,
            heuristic_func,
            opponent_player_char,
            node_counter,  # Pass the counter
        )
        if eval_score > max_eval:
            max_eval = eval_score
            best_move = move
        alpha = max(alpha, eval_score)  # Update alpha for root node as well
    return best_move, node_counter.get_count()
