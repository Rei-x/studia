import sys
import time
import random
import argparse
from math import inf

from astar_time_przesiadki import (
    load_data,
    build_graph,
    when_to_ride,
)
from utils import format_time, get_time_in_seconds


def calculate_route_cost(
    start_station,
    station_sequence,
    criteria,
    start_time,
    graph,
    station_coordinates,
    debug=False,
):
    """
    Calculate the cost of a route through the given sequence of stations.

    Args:
        start_station: Starting station
        station_sequence: List of stations to visit in sequence
        criteria: Optimization criteria ('t' for time, 'p' for transfers)
        start_time: Initial start time
        graph: Connection graph
        station_coordinates: Dictionary of station coordinates

    Returns:
        Tuple of (total_cost, total_path, is_valid)
    """
    total_path = []
    current_time = get_time_in_seconds(start_time)
    current_station = start_station
    total_transfers = 0

    # Complete sequence: start -> all stations -> back to start
    complete_sequence = station_sequence.copy()

    if debug:
        print(f"Evaluating sequence: {complete_sequence}")

    # Visit each station in sequence
    for next_station in complete_sequence:
        if debug:
            print(
                f"Finding route from {current_station} to {next_station} at {format_time(current_time)}"
            )

        # Find optimal route to next station
        arrival_time, path = when_to_ride(
            current_station,
            next_station,
            criteria,
            format_time(current_time),
            graph=graph,
            station_coordinates=station_coordinates,
            debug=debug,
        )

        if arrival_time == inf:
            if debug:
                print(f"No route found from {current_station} to {next_station}")
            return inf, [], False

        # Update current state
        if debug:
            print(f"Route found, arrival time: {format_time(arrival_time)}")

        current_time = arrival_time
        current_station = next_station
        total_path.extend(path)

        # Count transfers in this segment
        if criteria == "s" or criteria == "p":
            segment_transfers = len(set(ride[0] for ride in path)) - 1
            total_transfers += segment_transfers

    # Return to start station
    if debug:
        print(f"Finding route back from {current_station} to {start_station}")

    arrival_time, path = when_to_ride(
        current_station,
        start_station,
        criteria,
        format_time(current_time),
        graph=graph,
        station_coordinates=station_coordinates,
        debug=debug,
    )

    if arrival_time == inf:
        if debug:
            print("No route found back to start station")
        return inf, [], False

    if debug:
        print(f"Route found back to start, arrival time: {format_time(arrival_time)}")

    total_path.extend(path)

    # Calculate final cost based on criteria
    if criteria == "t":
        total_cost = arrival_time - get_time_in_seconds(start_time)
    else:  # criteria == 's' or criteria == 'p'
        # Add transfers for the return segment
        total_transfers += len(set(ride[0] for ride in path)) - 1
        total_cost = total_transfers

    return total_cost, total_path, True


def tabu_search(
    start_station,
    stations_to_visit,
    criteria,
    start_time,
    graph,
    station_coordinates,
    max_iterations=100,
    tabu_size=20,
    neighborhood_size=20,
    debug=False,
):
    """
    Use Tabu Search to find the optimal route visiting all stations and returning to start.

    Args:
        start_station: Starting and ending station
        stations_to_visit: List of stations that must be visited
        criteria: Optimization criteria ('t' for time, 'p' for transfers)
        start_time: Starting time in "HH:MM:SS" format
        graph: Graph representing connections
        station_coordinates: Dictionary of station coordinates
        max_iterations: Maximum number of iterations
        tabu_size: Size of the tabu list
        neighborhood_size: Number of neighbors to evaluate in each iteration

    Returns:
        Tuple of (best_cost, best_path)
    """
    if not stations_to_visit:
        return 0, []

    # Initialize with a random solution
    current_sequence = stations_to_visit.copy()
    random.shuffle(current_sequence)

    if debug:
        print(f"Initial sequence: {current_sequence}")

    # Calculate initial solution cost
    current_cost, current_path, is_valid = calculate_route_cost(
        start_station,
        current_sequence,
        criteria,
        start_time,
        graph,
        station_coordinates,
        debug,
    )

    if not is_valid:
        # If initial solution is not valid, try a few random sequences
        for _ in range(10):
            random.shuffle(current_sequence)
            current_cost, current_path, is_valid = calculate_route_cost(
                start_station,
                current_sequence,
                criteria,
                start_time,
                graph,
                station_coordinates,
                debug,
            )
            if is_valid:
                break

        if not is_valid:
            return inf, []  # No valid solution found

    # Best solution so far
    best_sequence = current_sequence.copy()
    best_cost = current_cost
    best_path = current_path

    if debug:
        print(f"Initial cost: {best_cost}")

    # Tabu list - store recently visited moves
    tabu_list = []

    # Main tabu search loop
    for iteration in range(max_iterations):
        if debug:
            print(f"\nIteration {iteration + 1}/{max_iterations}")
            print(f"Current sequence: {current_sequence}")
            print(f"Current cost: {current_cost}")

        # Generate and evaluate neighborhood
        best_neighbor_cost = inf
        best_neighbor_sequence = None
        best_neighbor_path = []

        # Try different neighbor generation strategies
        for _ in range(
            min(
                neighborhood_size,
                len(current_sequence) * (len(current_sequence) - 1) // 2,
            )
        ):
            # Randomly select the move type
            move_type = random.choice(["swap", "insert"])

            # Perform the selected move
            if move_type == "swap" and len(current_sequence) >= 2:
                # Swap two random positions
                i, j = random.sample(range(len(current_sequence)), 2)
                neighbor_sequence = current_sequence.copy()
                neighbor_sequence[i], neighbor_sequence[j] = (
                    neighbor_sequence[j],
                    neighbor_sequence[i],
                )
                move = ("swap", i, j)
            elif move_type == "insert" and len(current_sequence) >= 2:
                # Take element at position i and insert it at position j
                i = random.randrange(len(current_sequence))
                j = random.randrange(len(current_sequence))
                if i == j:
                    continue
                neighbor_sequence = current_sequence.copy()
                element = neighbor_sequence.pop(i)
                neighbor_sequence.insert(j, element)
                move = ("insert", i, j)
            else:
                continue

            # Skip if the move is in the tabu list
            if move in tabu_list:
                # Aspiration criteria - accept tabu move if it leads to a better solution
                if best_cost < inf:  # Only if we have a valid solution already
                    # Evaluate the neighbor
                    neighbor_cost, neighbor_path, is_valid = calculate_route_cost(
                        start_station,
                        neighbor_sequence,
                        criteria,
                        start_time,
                        graph,
                        station_coordinates,
                        debug=False,
                    )

                    # Accept if better than best solution
                    if is_valid and neighbor_cost < best_cost:
                        if debug:
                            print(
                                f"Accepting tabu move {move} due to aspiration criteria"
                            )
                        best_neighbor_cost = neighbor_cost
                        best_neighbor_sequence = neighbor_sequence
                        best_neighbor_path = neighbor_path
                        break  # Found a good solution via aspiration
                continue

            # Evaluate the neighbor
            neighbor_cost, neighbor_path, is_valid = calculate_route_cost(
                start_station,
                neighbor_sequence,
                criteria,
                start_time,
                graph,
                station_coordinates,
                debug=False,
            )

            if is_valid and neighbor_cost < best_neighbor_cost:
                best_neighbor_cost = neighbor_cost
                best_neighbor_sequence = neighbor_sequence
                best_neighbor_path = neighbor_path
                best_neighbor_move = move

        # If no valid neighbor found, try a random restart
        if best_neighbor_sequence is None:
            if debug:
                print("No valid neighbor found, trying random restart")
            current_sequence = stations_to_visit.copy()
            random.shuffle(current_sequence)
            current_cost, current_path, is_valid = calculate_route_cost(
                start_station,
                current_sequence,
                criteria,
                start_time,
                graph,
                station_coordinates,
                debug=False,
            )

            if not is_valid:
                continue
        else:
            # Move to the best neighbor
            current_sequence = best_neighbor_sequence
            current_cost = best_neighbor_cost
            current_path = best_neighbor_path

            # Add the move to the tabu list
            tabu_list.append(best_neighbor_move)
            if len(tabu_list) > tabu_size:
                tabu_list.pop(0)

            if debug:
                print(f"Moving to neighbor with cost {current_cost}")

        # Update best solution if improved
        if current_cost < best_cost:
            best_sequence = current_sequence.copy()
            best_cost = current_cost
            best_path = current_path

            if debug:
                print(f"New best solution found! Cost: {best_cost}")

    if debug:
        print(f"\nFinal best sequence: {best_sequence}")
        print(f"Final best cost: {best_cost}")

    return best_cost, best_path


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Find optimal route visiting multiple stations using Tabu Search"
    )
    parser.add_argument(
        "--start", default="Śliczna", help="Starting and ending station"
    )
    parser.add_argument(
        "--stations",
        default="Bezpieczna,Prudnicka",
        help="List of stations to visit",
    )
    parser.add_argument(
        "--method",
        choices=["t", "p"],
        default="t",
        help="Optimization criteria: t for time, p for transfers",
    )
    parser.add_argument(
        "--time", default="08:50:00", help="Starting time in HH:MM:SS format"
    )
    parser.add_argument(
        "--iterations", type=int, default=100, help="Maximum number of iterations"
    )
    parser.add_argument(
        "--tabu-size", type=int, default=20, help="Size of the tabu list"
    )
    parser.add_argument(
        "--neighborhood-size",
        type=int,
        default=20,
        help="Number of neighbors to evaluate in each iteration",
    )

    args = parser.parse_args()

    # Map 'p' criteria to 's' for the when_to_ride function
    search_criteria = args.method

    # Start timer

    # Load data and build graph
    df = load_data()
    graph, station_coordinates = build_graph(df)

    start_timer = time.time()
    # Run tabu search
    best_cost, best_path = tabu_search(
        args.start,
        args.stations.split(","),
        search_criteria,
        args.time,
        graph,
        station_coordinates,
        max_iterations=args.iterations,
        tabu_size=args.tabu_size,
        neighborhood_size=args.neighborhood_size,
    )

    # End timer
    end_timer = time.time()
    computation_time = end_timer - start_timer

    # Output results
    if best_cost == inf or not best_path:
        print("No valid route found")
        print("Cost: inf", file=sys.stderr)
    else:
        # Print the route details
        for ride in best_path:
            line_name, board_stop, board_time, alight_stop, alight_time = ride
            formatted_board_time = format_time(board_time)
            formatted_alight_time = format_time(alight_time)
            print(
                f"{line_name}, {formatted_board_time}, {board_stop}, {formatted_alight_time}, {alight_stop}"
            )

        # Print cost and computation time to stderr
        print(f"Cost: {best_cost}", file=sys.stderr)

    print(f"Computation time: {computation_time:.2f} seconds", file=sys.stderr)


if __name__ == "__main__":
    main()
