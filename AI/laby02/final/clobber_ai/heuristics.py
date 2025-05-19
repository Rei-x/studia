from .board import Board  # Use relative import


# Heuristic functions
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
    return piece_weight * h_piece_difference(
        board, player_char_perspective
    ) + mobility_weight * h_mobility_difference(board, player_char_perspective)


def h_adaptive_strategy(board: Board, player_char_perspective: str):
    my_pieces = 0
    opponent_pieces = 0
    opponent_char = board.get_opponent(player_char_perspective)
    for r in range(board.rows):
        for c in range(board.cols):
            if board.grid[r][c] == player_char_perspective:
                my_pieces += 1
            elif board.grid[r][c] == opponent_char:
                opponent_pieces += 1
    total_pieces = my_pieces + opponent_pieces
    my_mobility = len(board.get_possible_moves(player_char_perspective))
    opponent_mobility = len(board.get_possible_moves(opponent_char))
    total_mobility = my_mobility + opponent_mobility
    is_endgame = (total_pieces < (board.rows * board.cols) * 0.4) or (
        total_mobility < (board.rows + board.cols) * 0.6
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
