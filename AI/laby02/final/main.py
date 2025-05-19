# clobber_project/main.py
import sys
import argparse
import questionary  # Keep for interactive setup

# Import from the clobber_ai package
from clobber_ai.heuristics import HEURISTICS_MAP
from clobber_ai.game_logic import (
    play_game,
)  # play_game now uses algorithms from its module


def get_player_settings_interactive(player_num_str: str, player_name: str):
    print(
        f"\n--- Settings for Player {player_num_str} ({player_name}) ---",
        file=sys.stderr,
    )
    sys.stderr.flush()
    heuristic_choices = list(HEURISTICS_MAP.keys())
    chosen_heuristic_name = questionary.select(
        f"Choose heuristic for Player {player_num_str} ({player_name}):",
        choices=heuristic_choices,
    ).ask()
    if chosen_heuristic_name is None:
        sys.exit("Setup cancelled by user.")
    search_depth_str = questionary.text(
        f"Enter max search depth (d) for Player {player_num_str} (e.g., 3):",
        default="3",
        validate=lambda text: text.isdigit()
        and int(text) > 0
        or "Please enter a positive integer.",
    ).ask()
    if search_depth_str is None:
        sys.exit("Setup cancelled by user.")
    search_depth = int(search_depth_str)
    algo_choices = ["minimax", "alphabeta"]  # These are known by game_logic/algorithms
    algo_choice = questionary.select(
        f"Choose algorithm for Player {player_num_str} ({player_name}):",
        choices=algo_choices,
    ).ask()
    if algo_choice is None:
        sys.exit("Setup cancelled by user.")
    return algo_choice, chosen_heuristic_name, search_depth


def positive_int(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f"{value} is an invalid positive int value")
    return ivalue


def main():
    parser = argparse.ArgumentParser(description="Clobber AI Game")
    parser.add_argument(
        "--p1_algo",
        choices=["minimax", "alphabeta"],
        default="alphabeta",
        help="Algorithm for Player 1 (Black)",
    )
    parser.add_argument(
        "--p1_heuristic",
        choices=list(HEURISTICS_MAP.keys()),
        default="adaptive",
        help="Heuristic for Player 1 (Black)",
    )
    parser.add_argument(
        "--p1_depth",
        type=positive_int,
        default=3,
        help="Search depth for Player 1 (Black)",
    )
    parser.add_argument(
        "--p2_algo",
        choices=["minimax", "alphabeta"],
        default="alphabeta",
        help="Algorithm for Player 2 (White)",
    )
    parser.add_argument(
        "--p2_heuristic",
        choices=list(HEURISTICS_MAP.keys()),
        default="adaptive",
        help="Heuristic for Player 2 (White)",
    )
    parser.add_argument(
        "--p2_depth",
        type=positive_int,
        default=3,
        help="Search depth for Player 2 (White)",
    )
    parser.add_argument(
        "--board_file",
        type=str,
        default=None,
        help="Path to a file representing the initial board state.",
    )
    parser.add_argument(
        "--interactive_setup",
        action="store_true",
        help="Force interactive setup for players, ignoring other p1/p2 CLI args.",
    )
    parser.add_argument(
        "--rows",
        type=int,
        default=0,  # Will be inferred or default to 5 if no board string
        help="Number of board rows (used if no board_file/stdin and for default setup).",
    )
    parser.add_argument(
        "--cols",
        type=int,
        default=0,  # Will be inferred or default to 6 if no board string
        help="Number of board columns (used if no board_file/stdin and for default setup).",
    )

    args = parser.parse_args()

    default_rows, default_cols = 5, 6
    game_board_str = None

    # Determine rows and cols for Board initialization
    # If board_file or stdin is used, Board will try to parse dimensions.
    # If not, use CLI args or defaults.
    current_rows = args.rows if args.rows > 0 else default_rows
    current_cols = args.cols if args.cols > 0 else default_cols

    if args.board_file:
        try:
            with open(args.board_file, "r") as f:
                game_board_str = f.read().strip()
            if not game_board_str:
                print(
                    f"Warning: Board file '{args.board_file}' is empty. Using default dimensions {current_rows}x{current_cols}.",
                    file=sys.stderr,
                )
                game_board_str = None  # Will trigger default setup in Board class
            else:
                # Board class will parse rows/cols from this string
                # Set current_rows/cols to 0 to signal Board to infer
                current_rows, current_cols = 0, 0
                print(f"Using board from file: {args.board_file}", file=sys.stderr)
        except FileNotFoundError:
            print(
                f"Error: Board file '{args.board_file}' not found. Using default dimensions {current_rows}x{current_cols}.",
                file=sys.stderr,
            )
            game_board_str = None
        except Exception as e:
            print(
                f"Error reading board file '{args.board_file}': {e}. Using default dimensions {current_rows}x{current_cols}.",
                file=sys.stderr,
            )
            game_board_str = None
    elif not sys.stdin.isatty():  # Check for piped input only if no board_file
        piped_input = sys.stdin.read().strip()
        if piped_input:
            game_board_str = piped_input
            current_rows, current_cols = 0, 0  # Signal Board to infer
            print("Using board from piped stdin.", file=sys.stderr)
        else:
            print(
                f"Piped stdin was empty. Using default dimensions {current_rows}x{current_cols}.",
                file=sys.stderr,
            )
            game_board_str = None  # Will trigger default setup

    if game_board_str is None:
        print(
            f"Using default Clobber board {current_rows}x{current_cols}.",
            file=sys.stderr,
        )

    sys.stderr.flush()

    if args.interactive_setup:
        if not questionary:
            print(
                "Error: 'questionary' library is required for interactive setup but not found.",
                file=sys.stderr,
            )
            print("Please install it: pip install questionary", file=sys.stderr)
            print(
                "You can run without --interactive_setup to use CLI arguments.",
                file=sys.stderr,
            )
            sys.exit(1)
        print("Interactive setup chosen.", file=sys.stderr)
        p1_algo, p1_heuristic, p1_depth = get_player_settings_interactive("1", "Black")
        p2_algo, p2_heuristic, p2_depth = get_player_settings_interactive("2", "White")
    else:
        p1_algo, p1_heuristic, p1_depth = args.p1_algo, args.p1_heuristic, args.p1_depth
        p2_algo, p2_heuristic, p2_depth = args.p2_algo, args.p2_heuristic, args.p2_depth
        print("Using player settings from CLI arguments or defaults:", file=sys.stderr)
        print(
            f"  P1 (Black): {p1_algo}, {p1_heuristic}, depth {p1_depth}",
            file=sys.stderr,
        )
        print(
            f"  P2 (White): {p2_algo}, {p2_heuristic}, depth {p2_depth}",
            file=sys.stderr,
        )

    print("\nStarting game...", file=sys.stderr)
    sys.stderr.flush()

    try:
        play_game(
            initial_board_str=game_board_str,  # Can be None for default setup
            rows=current_rows,  # Board class handles these
            cols=current_cols,
            p1_algo_choice=p1_algo,
            p1_heuristic_name=p1_heuristic,
            p1_depth=p1_depth,
            p2_algo_choice=p2_algo,
            p2_heuristic_name=p2_heuristic,
            p2_depth=p2_depth,
        )
    except ValueError as e:
        print(f"Error during game setup or play: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
