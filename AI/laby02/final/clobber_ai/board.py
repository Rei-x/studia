# clobber_project/clobber_ai/board.py
import sys
from .constants import BLACK, WHITE, EMPTY  # Use relative import


class Board:
    def __init__(self, rows, cols, initial_board_str=None):
        self.rows = rows
        self.cols = cols
        if initial_board_str:
            self.grid = self._parse_board_str(initial_board_str)
        else:
            if not (
                self.rows > 0 and self.cols > 0
            ):  # Ensure dimensions are set if no string
                # This case can happen if rows/cols are passed as 0 initially
                # and no board_str is given to infer them.
                # Let's assume a default if this happens, or raise error earlier.
                # For now, the main.py logic handles setting rows/cols before this.
                # If initial_board_str is None, _default_clobber_setup will be called
                # which has its own check.
                pass
            self.grid = self._default_clobber_setup()

    def _parse_board_str(self, board_str):
        grid = []
        lines = board_str.strip().split("\n")

        # Infer dimensions if not pre-set (rows/cols might be 0 initially)
        parsed_rows = len(lines)
        parsed_cols = 0
        if parsed_rows > 0 and lines[0].strip():  # Check if first line is not empty
            parsed_cols = len(lines[0].split())

        if self.rows == 0 and parsed_rows > 0:
            self.rows = parsed_rows
        elif self.rows > 0 and parsed_rows != self.rows:
            raise ValueError(
                f"Board string has {parsed_rows} rows, expected {self.rows} from pre-set value."
            )

        if self.cols == 0 and parsed_cols > 0:
            self.cols = parsed_cols
        elif (
            self.cols > 0 and parsed_cols != self.cols and parsed_cols > 0
        ):  # only error if parsed_cols is valid but different
            raise ValueError(
                f"Board string has {parsed_cols} cols, expected {self.cols} from pre-set value."
            )

        if self.rows == 0 or self.cols == 0:  # If still zero after trying to parse
            raise ValueError(
                f"Could not determine board dimensions. Current: rows={self.rows}, cols={self.cols}"
            )

        for r_idx, line in enumerate(lines):
            pieces = line.split()
            if len(pieces) != self.cols:
                raise ValueError(
                    f"Board string line {r_idx} has {len(pieces)} pieces, expected {self.cols} columns. Line content: '{line}'"
                )
            grid.append(list(pieces))
        return grid

    def _default_clobber_setup(self):
        if not (self.rows > 0 and self.cols > 0):
            # This should ideally be caught before calling if default is intended
            # For example, main.py sets default_rows/cols if no board_str
            raise ValueError(
                f"Board dimensions must be positive for default setup. Got rows={self.rows}, cols={self.cols}"
            )

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
        file.flush()

    def get_opponent(self, player_char):
        return WHITE if player_char == BLACK else BLACK

    def is_valid_pos(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols

    def copy(self):
        # Create a new Board instance and copy grid
        # This ensures that if initial_board_str was used, it's not re-parsed unnecessarily
        new_board = Board(self.rows, self.cols)  # Will call _default_clobber_setup
        new_board.grid = [row[:] for row in self.grid]  # Then overwrite grid
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
        # Basic validation (optional, assuming moves are generated correctly)
        # if not self.is_valid_pos(from_r, from_c) or not self.is_valid_pos(to_r, to_c):
        #     raise ValueError(f"Invalid move coordinates: {move}")
        # if self.grid[from_r][from_c] != player_char:
        #     raise ValueError(f"No piece of player {player_char} at {from_r},{from_c}")
        # if self.grid[to_r][to_c] != self.get_opponent(player_char):
        #     raise ValueError(f"Target square {to_r},{to_c} does not contain opponent's piece.")

        self.grid[to_r][to_c] = player_char
        self.grid[from_r][from_c] = EMPTY
