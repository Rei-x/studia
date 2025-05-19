# filepath: /home/rei/projects/studia/AI/laby02/main_test.py
import unittest

# If main.py is in the same directory, this direct import should work.
# If you run tests from a different directory or structure, sys.path adjustments might be needed.
from laby02.main_v0 import (
    ClobberGame,
    PLAYER_B,
    PLAYER_W,
    EMPTY,
    heuristic_piece_difference,
    heuristic_mobility_difference,
    heuristic_combined_score,
    get_best_move_minimax,
    get_best_move_alphabeta,
    minimax,  # Import for direct testing of terminal/depth 0 cases
    minimax_alphabeta,  # Import for direct testing of terminal/depth 0 cases
    # VISITED_NODES is a global in main, will be accessed via main_module.VISITED_NODES
)

# It's cleaner to import the module itself to manage globals like VISITED_NODES
import laby02.main_v0 as main_module


class TestClobberGame(unittest.TestCase):
    def test_board_parsing_and_initialization(self):
        board_str = "B W\nW B"
        game = ClobberGame(board_str, PLAYER_B)
        self.assertEqual(game.rows, 2)
        self.assertEqual(game.cols, 2)
        self.assertEqual(game.board, [["B", "W"], ["W", "B"]])
        self.assertEqual(game.current_player, PLAYER_B)

    def test_str_representation(self):
        board_str = "B W\nW B"
        game = ClobberGame(board_str)
        self.assertEqual(str(game), board_str)

    def test_get_opponent(self):
        game = ClobberGame("B W", PLAYER_B)  # Minimal board for this test
        self.assertEqual(game.get_opponent(PLAYER_B), PLAYER_W)
        self.assertEqual(game.get_opponent(PLAYER_W), PLAYER_B)

    def test_get_possible_moves_simple(self):
        board_str = "B W\n_ _"
        game = ClobberGame(board_str, PLAYER_B)
        moves_b = game.get_possible_moves(PLAYER_B)
        self.assertEqual(len(moves_b), 1)
        self.assertIn(((0, 0), (0, 1)), moves_b)

        # Test for Player W
        game_w_turn = ClobberGame(board_str, PLAYER_W)
        moves_w = game_w_turn.get_possible_moves(PLAYER_W)
        self.assertEqual(len(moves_w), 1)
        # W at (0,1) captures B at (0,0)
        self.assertIn(((0, 1), (0, 0)), moves_w)

    def test_get_possible_moves_none(self):
        # Board where Player B has no W pieces to capture
        board_str_b_no_moves = "B B\nB B"
        game_b = ClobberGame(board_str_b_no_moves, PLAYER_B)
        moves_b = game_b.get_possible_moves(PLAYER_B)
        self.assertEqual(
            len(moves_b),
            0,
            "Player B should have 0 moves on a board with no opponents to capture.",
        )

        # Board where Player W has no B pieces to capture
        board_str_w_no_moves = "W W\nW W"
        game_w = ClobberGame(board_str_w_no_moves, PLAYER_W)
        moves_w = game_w.get_possible_moves(PLAYER_W)
        self.assertEqual(
            len(moves_w),
            0,
            "Player W should have 0 moves on a board with no opponents to capture.",
        )

        # Another scenario: B is blocked by its own pieces or empty spaces from reaching W
        board_str_b_blocked = "B _ B\n_ _ _\nW _ W"  # B at (0,0) and (0,2) cannot reach W at (2,0) or (2,2)
        game_b_blocked = ClobberGame(board_str_b_blocked, PLAYER_B)
        moves_b_blocked = game_b_blocked.get_possible_moves(PLAYER_B)
        self.assertEqual(
            len(moves_b_blocked), 0, "Player B should have 0 moves when blocked from W."
        )

    def test_get_possible_moves_complex(self):
        board_str = "B W B\nW B W\nB W B"
        game_b_turn = ClobberGame(board_str, PLAYER_B)
        moves_b = game_b_turn.get_possible_moves(PLAYER_B)
        # Expected moves for B:
        # (0,0) -> (0,1), (1,0)
        # (0,2) -> (0,1), (1,2)
        # (1,1) -> (0,1), (1,0), (1,2), (2,1)
        # (2,0) -> (1,0), (2,1)
        # (2,2) -> (1,2), (2,1)
        # Total = 2 + 2 + 4 + 2 + 2 = 12
        self.assertEqual(len(moves_b), 12)

        game_w_turn = ClobberGame(board_str, PLAYER_W)
        moves_w = game_w_turn.get_possible_moves(PLAYER_W)
        self.assertEqual(len(moves_w), 12)  # Symmetric board

    def test_make_move(self):
        board_str = "B W\n_ _"
        game = ClobberGame(board_str, PLAYER_B)
        move = ((0, 0), (0, 1))  # B captures W
        new_game_state = game.make_move(move)

        self.assertEqual(new_game_state.board[0][0], EMPTY)
        self.assertEqual(new_game_state.board[0][1], PLAYER_B)
        self.assertEqual(new_game_state.current_player, PLAYER_W)
        # Ensure original game state is unchanged
        self.assertEqual(game.board[0][0], PLAYER_B)
        self.assertEqual(game.board[0][1], PLAYER_W)
        self.assertEqual(game.current_player, PLAYER_B)

    def test_is_game_over_false(self):
        board_str = "B W\n_ _"
        game = ClobberGame(board_str, PLAYER_B)
        self.assertFalse(game.is_game_over())

    def test_is_game_over_true(self):
        board_str_b_no_moves = "B B\n_ _"  # Player B has no W to capture
        game_b_no_moves = ClobberGame(board_str_b_no_moves, PLAYER_B)
        self.assertTrue(game_b_no_moves.is_game_over())

        board_str_w_no_moves = "W W\n_ _"  # Player W has no B to capture
        game_w_no_moves = ClobberGame(board_str_w_no_moves, PLAYER_W)
        self.assertTrue(game_w_no_moves.is_game_over())

    def test_get_winner(self):
        # get_winner simply returns the player passed to it, as per Clobber rules.
        game = ClobberGame("B W", PLAYER_B)  # Minimal board
        self.assertEqual(game.get_winner(PLAYER_B), PLAYER_B)
        self.assertEqual(game.get_winner(PLAYER_W), PLAYER_W)


class TestHeuristics(unittest.TestCase):
    def test_heuristic_piece_difference(self):
        board_str_b_more = "B B W\nB _ _"
        game_b_more = ClobberGame(board_str_b_more, PLAYER_B)
        # B: 3, W: 1. Diff for B = 3 - 1 = 2
        self.assertEqual(heuristic_piece_difference(game_b_more, PLAYER_B), 2)
        # Diff for W = 1 - 3 = -2
        self.assertEqual(heuristic_piece_difference(game_b_more, PLAYER_W), -2)

        board_str_equal = "B W\nW B"
        game_equal = ClobberGame(board_str_equal, PLAYER_B)
        # B: 2, W: 2. Diff for B = 2 - 2 = 0
        self.assertEqual(heuristic_piece_difference(game_equal, PLAYER_B), 0)

    def test_heuristic_mobility_difference(self):
        board_str = "B W\n_ _"
        game = ClobberGame(board_str, PLAYER_B)
        # Moves for B: 1 ((0,0)->(0,1)). Moves for W: 1 ((0,1)->(0,0)).
        # Diff for B = 1 (B's moves) - 1 (W's moves) = 0
        self.assertEqual(heuristic_mobility_difference(game, PLAYER_B), 0)
        # Diff for W = 1 (W's moves) - 1 (B's moves) = 0
        self.assertEqual(heuristic_mobility_difference(game, PLAYER_W), 0)

        board_str_complex = "B W _\nB _ _\nW _ _"
        game_complex = ClobberGame(board_str_complex, PLAYER_B)
        # For PLAYER_B evaluation:
        # B moves: ((0,0)->(0,1) to capture W), ((1,0)->(2,0) to capture W) = 2 moves
        # W moves: ((0,1)->(0,0) to capture B), ((2,0)->(1,0) to capture B) = 2 moves
        # Diff for B = 2 (B's moves) - 2 (W's moves) = 0
        self.assertEqual(heuristic_mobility_difference(game_complex, PLAYER_B), 0)

        # For PLAYER_W evaluation:
        # W moves: ((0,1)->(0,0)), ((2,0)->(1,0)) = 2 moves
        # B moves: ((0,0)->(0,1)), ((1,0)->(2,0)) = 2 moves
        # Diff for W = 2 (W's moves) - 2 (B's moves) = 0
        self.assertEqual(heuristic_mobility_difference(game_complex, PLAYER_W), 0)

    def test_heuristic_combined_score(self):
        # B: 2 pieces (at (0,0), (1,0)), W: 1 piece (at (0,1)).
        # Piece diff for B = 2 - 1 = 1.
        # B moves: ((0,0)->(0,1)) = 1. W moves: ((0,1)->(0,0)) = 1. Mobility diff for B = 1 - 1 = 0.
        # Combined for B = (1.0 * 1) + (2.0 * 0) = 1.0
        board_str = "B W\nB _"
        game = ClobberGame(board_str, PLAYER_B)
        self.assertEqual(heuristic_combined_score(game, PLAYER_B), 1.0 * 1 + 2.0 * 0)

        # Piece diff for W = 1 - 2 = -1.
        # W moves: 1. B moves: 1. Mobility diff for W = 1 - 1 = 0.
        # Combined for W = (1.0 * -1) + (2.0 * 0) = -1.0
        self.assertEqual(heuristic_combined_score(game, PLAYER_W), 1.0 * (-1) + 2.0 * 0)


class TestAlgorithms(unittest.TestCase):
    def setUp(self):
        # Reset VISITED_NODES before each algorithm test
        main_module.VISITED_NODES = 0

    def test_minimax_simple_win_depth1(self):
        # B W -> B captures W, board becomes _ B. B has 1 piece, W has 0. Heuristic for B = 1.
        board_str = "B W"
        game = ClobberGame(board_str, PLAYER_B)
        best_move = get_best_move_minimax(game, 1, PLAYER_B, heuristic_piece_difference)
        self.assertEqual(best_move, ((0, 0), (0, 1)))

    def test_alphabeta_simple_win_depth1(self):
        board_str = "B W"
        game = ClobberGame(board_str, PLAYER_B)
        best_move = get_best_move_alphabeta(
            game, 1, PLAYER_B, heuristic_piece_difference
        )
        self.assertEqual(best_move, ((0, 0), (0, 1)))

    def test_minimax_depth1_choice_of_two_equal_moves(self):
        # B W _ -> move ((0,0),(0,1)) -> _ B _ (score 1 for B)
        # _ W B -> move ((1,2),(1,1)) -> _ B _ (score 1 for B)
        # Both lead to one B, zero W. Minimax might pick the first valid one.
        board_str = "B W _\n_ W B"
        game = ClobberGame(board_str, PLAYER_B)
        # Possible moves for B: ((0,0),(0,1)) and ((1,2),(1,1))
        # After ((0,0),(0,1)): _ B _ \n _ W B. Heuristic for B (piece_diff): B=2, W=1. Score = 1
        # After ((1,2),(1,1)): B W _ \n _ B _. Heuristic for B (piece_diff): B=2, W=1. Score = 1
        # Both moves are equivalent by piece_difference heuristic at depth 1.
        best_move = get_best_move_minimax(game, 1, PLAYER_B, heuristic_piece_difference)
        self.assertIn(best_move, [((0, 0), (0, 1)), ((1, 2), (1, 1))])

    def test_alphabeta_depth1_choice_of_two_equal_moves(self):
        board_str = "B W _\n_ W B"
        game = ClobberGame(board_str, PLAYER_B)
        best_move = get_best_move_alphabeta(
            game, 1, PLAYER_B, heuristic_piece_difference
        )
        self.assertIn(best_move, [((0, 0), (0, 1)), ((1, 2), (1, 1))])

    def test_minimax_forced_win_depth2(self):
        # Board: W B _
        #        _ W _
        # B to move. Depth 2. Heuristic: piece_difference.
        # B moves ((0,1) to (0,0)): Captures W. Board: B _ _ \n _ W _. B player, score for B: 1-1=0.
        #   Now W's turn. W at (1,1) has no moves. Game over. B (previous player) wins. Score: +inf.
        # This is an immediate win for B.
        board_str = "W B _\n_ W _"
        game = ClobberGame(board_str, PLAYER_B)
        best_move = get_best_move_minimax(game, 2, PLAYER_B, heuristic_piece_difference)
        self.assertEqual(best_move, ((0, 1), (0, 0)))

    def test_alphabeta_forced_win_depth2(self):
        board_str = "W B _\n_ W _"
        game = ClobberGame(board_str, PLAYER_B)
        best_move = get_best_move_alphabeta(
            game, 2, PLAYER_B, heuristic_piece_difference
        )
        self.assertEqual(best_move, ((0, 1), (0, 0)))

    def test_minimax_vs_alphabeta_consistency_and_nodes(self):
        board_str = "B W B W\nW B W B\nB W B W\nW B W B"
        game = ClobberGame(board_str, PLAYER_B)
        depth = 2  # Keep depth low for reasonable test time

        main_module.VISITED_NODES = 0
        best_move_mm = get_best_move_minimax(
            game, depth, PLAYER_B, heuristic_combined_score
        )
        nodes_mm = main_module.VISITED_NODES

        main_module.VISITED_NODES = 0
        best_move_ab = get_best_move_alphabeta(
            game, depth, PLAYER_B, heuristic_combined_score
        )
        nodes_ab = main_module.VISITED_NODES

        self.assertEqual(
            best_move_mm,
            best_move_ab,
            "Minimax and AlphaBeta should yield the same best move.",
        )
        # Alpha-beta should not visit more nodes than minimax.
        # It can be equal if no pruning occurs, or less if pruning happens.
        if (
            best_move_mm is not None
        ):  # Only check node count if a game is playable and moves are found
            self.assertLessEqual(
                nodes_ab,
                nodes_mm,
                f"AlphaBeta visited {nodes_ab} nodes, Minimax visited {nodes_mm} nodes.",
            )

    def test_game_over_terminal_evaluation_minimax(self):
        # State where current player W has no moves. So B (AI player) wins.
        game_state_w_no_moves = ClobberGame(
            "B B\nB B", PLAYER_W
        )  # W is current, but has no moves.
        main_module.VISITED_NODES = 0
        # minimax(game_state, depth, maximizing_player_is_ai_player, ai_player, chosen_heuristic_func, current_player_for_move)
        # ai_player = B, current_player_for_move = W. W has no moves. B wins.
        val, _ = minimax(
            game_state_w_no_moves,
            1,
            True,
            PLAYER_B,
            heuristic_piece_difference,
            PLAYER_W,
        )
        self.assertEqual(
            val, float("inf"), "AI (B) should get +inf if opponent (W) has no moves."
        )

        main_module.VISITED_NODES = 0
        # ai_player = W, current_player_for_move = W. W has no moves. W loses.
        val, _ = minimax(
            game_state_w_no_moves,
            1,
            True,
            PLAYER_W,
            heuristic_piece_difference,
            PLAYER_W,
        )
        self.assertEqual(
            val, float("-inf"), "AI (W) should get -inf if AI (W) has no moves."
        )

    def test_game_over_terminal_evaluation_alphabeta(self):
        game_state_w_no_moves = ClobberGame("B B\nB B", PLAYER_W)
        main_module.VISITED_NODES = 0
        # minimax_alphabeta(game_state, depth, alpha, beta, maximizing_player_is_ai_player, ai_player, chosen_heuristic_func, current_player_for_move)
        val, _ = minimax_alphabeta(
            game_state_w_no_moves,
            1,
            float("-inf"),
            float("inf"),
            True,
            PLAYER_B,
            heuristic_piece_difference,
            PLAYER_W,
        )
        self.assertEqual(val, float("inf"))

        main_module.VISITED_NODES = 0
        val, _ = minimax_alphabeta(
            game_state_w_no_moves,
            1,
            float("-inf"),
            float("inf"),
            True,
            PLAYER_W,
            heuristic_piece_difference,
            PLAYER_W,
        )
        self.assertEqual(val, float("-inf"))

    def test_depth_zero_evaluation_minimax(self):
        board_str = "B W\n_ B"  # B:2, W:1. For PLAYER_B, piece_diff = 1
        game = ClobberGame(board_str, PLAYER_B)
        main_module.VISITED_NODES = 0
        val, _ = minimax(game, 0, True, PLAYER_B, heuristic_piece_difference, PLAYER_B)
        self.assertEqual(val, heuristic_piece_difference(game, PLAYER_B))
        self.assertEqual(val, 1)
        self.assertEqual(
            main_module.VISITED_NODES, 1
        )  # Depth 0 means one node visit (the root for this call)

    def test_depth_zero_evaluation_alphabeta(self):
        board_str = "B W\n_ B"
        game = ClobberGame(board_str, PLAYER_B)
        main_module.VISITED_NODES = 0
        val, _ = minimax_alphabeta(
            game,
            0,
            float("-inf"),
            float("inf"),
            True,
            PLAYER_B,
            heuristic_piece_difference,
            PLAYER_B,
        )
        self.assertEqual(val, heuristic_piece_difference(game, PLAYER_B))
        self.assertEqual(val, 1)
        self.assertEqual(main_module.VISITED_NODES, 1)


if __name__ == "__main__":
    # To run tests from the command line:
    # Ensure main.py and main_test.py are in the same directory.
    # Navigate to this directory in the terminal.
    # Run: python -m unittest main_test.py
    unittest.main()
