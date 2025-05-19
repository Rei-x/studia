# clobber_project/clobber_ai/__init__.py
from .board import Board
from .constants import BLACK, WHITE, EMPTY, WIN_SCORE, LOSS_SCORE
from .heuristics import (
    HEURISTICS_MAP,
    h_piece_difference,
    h_mobility_difference,
    h_combined_piece_mobility,
    h_adaptive_strategy,
)
from .algorithms import find_best_move_minimax, find_best_move_alphabeta
from .game_logic import play_game

# This allows: from clobber_ai import Board, play_game, etc.
# instead of from clobber_ai.board import Board

__all__ = [
    "Board",
    "BLACK",
    "WHITE",
    "EMPTY",
    "WIN_SCORE",
    "LOSS_SCORE",
    "HEURISTICS_MAP",
    "h_piece_difference",
    "h_mobility_difference",
    "h_combined_piece_mobility",
    "h_adaptive_strategy",
    "find_best_move_minimax",
    "find_best_move_alphabeta",
    "play_game",
]
