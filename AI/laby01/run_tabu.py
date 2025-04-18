import sys
import time
import random
import argparse
from math import inf, sqrt

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


def calculate_optimal_tabu_size(stations_count):
    """
    Calculate the optimal tabu list size based on the number of stations.

    The size is calculated using a combination of factors:
    - The number of possible swaps grows quadratically with the number of stations
    - We want to avoid cycling while also not wasting memory

    Args:
        stations_count: Number of stations in the route

    Returns:
        Optimal tabu list size
    """
    if stations_count <= 1:
        return 1

    # Calculate possible number of moves (swaps and inserts)
    possible_swaps = stations_count * (stations_count - 1) // 2
    possible_inserts = stations_count * (stations_count - 1)

    # Base the tabu size on the number of possible moves
    # Using a square root relationship to balance between too small and too large
    base_size = int(sqrt(possible_swaps + possible_inserts))

    # Ensure a minimum and maximum size
    return max(5, min(base_size, 50))


def aspiration_function(
    neighbor_cost, current_cost, best_cost, iteration, max_iterations
):
    """
    Determine whether a tabu move should be accepted based on aspiration criteria.

    Args:
        neighbor_cost: Cost of the neighbor solution
        current_cost: Cost of the current solution
        best_cost: Cost of the best solution found so far
        iteration: Current iteration number
        max_iterations: Maximum number of iterations

    Returns:
        Boolean indicating whether to accept the tabu move
    """
    # Accept tabu moves that improve the best solution
    if neighbor_cost < best_cost:
        return True

    # Accept tabu moves that are significantly better than the current solution
    # (even if not better than the global best)
    improvement_threshold = 0.05  # 5% improvement
    if neighbor_cost < current_cost * (1 - improvement_threshold):
        return True

    # Accept more tabu moves in later iterations to escape local optima
    # (increases diversification in later stages of search)
    if iteration > 0.7 * max_iterations and random.random() < 0.3:
        return True

    return False


def generate_neighbors(current_sequence, tabu_list, strategy="vertex", debug=False):
    """
    Generate neighbors based on the selected strategy.

    Args:
        current_sequence: Current sequence of stations
        tabu_list: List of tabu moves
        strategy: Strategy for generating neighbors ('vertex', 'edge', 'edge_vertex')
        debug: Enable debug output

    Returns:
        List of tuples (neighbor_sequence, move)
    """
    neighbors = []
    n = len(current_sequence)

    if strategy == "vertex":
        # Prohibit specific vertices at specific positions
        for i in range(n):
            for j in range(n):
                if i != j:
                    neighbor_sequence = current_sequence.copy()
                    neighbor_sequence[i], neighbor_sequence[j] = (
                        neighbor_sequence[j],
                        neighbor_sequence[i],
                    )
                    move = ("vertex", i, j)
                    if move not in tabu_list:
                        neighbors.append((neighbor_sequence, move))

    elif strategy == "edge":
        # Prohibit specific edges (pairs of consecutive vertices)
        for i in range(n - 1):
            for j in range(i + 1, n):
                neighbor_sequence = current_sequence.copy()
                neighbor_sequence[i : j + 1] = reversed(neighbor_sequence[i : j + 1])
                move = ("edge", i, j)
                if move not in tabu_list:
                    neighbors.append((neighbor_sequence, move))

    elif strategy == "edge_vertex":
        # Prohibit edges involving specific vertices
        for i in range(n):
            for j in range(i + 1, n):
                neighbor_sequence = current_sequence.copy()
                neighbor_sequence[i], neighbor_sequence[j] = (
                    neighbor_sequence[j],
                    neighbor_sequence[i],
                )
                move = ("edge_vertex", i, j)
                if move not in tabu_list:
                    neighbors.append((neighbor_sequence, move))

    if debug:
        print(f"Generated {len(neighbors)} neighbors using strategy '{strategy}'")

    return neighbors


def tabu_search(
    start_station,
    stations_to_visit,
    criteria,
    start_time,
    graph,
    station_coordinates,
    max_iterations=100,
    tabu_size=None,
    neighborhood_size=20,
    sampling_strategy="vertex",
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
        tabu_size: Size of the tabu list (if None, will be calculated dynamically)
        neighborhood_size: Number of neighbors to evaluate in each iteration
        sampling_strategy: Strategy for generating neighbors ('vertex', 'edge', 'edge_vertex')
        debug: Enable debug output

    Returns:
        Tuple of (best_cost, best_path)
    """
    if not stations_to_visit:
        return 0, []

    # Calculate optimal tabu size if not specified
    if tabu_size is None:
        tabu_size = calculate_optimal_tabu_size(len(stations_to_visit))
        if debug:
            print(f"Dynamically calculated tabu size: {tabu_size}")

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

    # Keep track of aspiration acceptances for statistics
    aspiration_acceptances = 0

    # Main tabu search loop
    for iteration in range(max_iterations):
        if debug:
            print(f"\nIteration {iteration + 1}/{max_iterations}")
            print(f"Current sequence: {current_sequence}")
            print(f"Current cost: {current_cost}")

        # Generate neighbors using the selected strategy
        neighbors = generate_neighbors(
            current_sequence, tabu_list, sampling_strategy, debug
        )

        # Evaluate neighbors
        best_neighbor_cost = inf
        best_neighbor_sequence = None
        best_neighbor_path = []
        best_neighbor_move = None

        for neighbor_sequence, move in neighbors[:neighborhood_size]:
            neighbor_cost, neighbor_path, is_valid = calculate_route_cost(
                start_station,
                neighbor_sequence,
                criteria,
                start_time,
                graph,
                station_coordinates,
                debug=False,
            )

            if not is_valid:
                continue

            # Check if the move is in the tabu list
            is_tabu = move in tabu_list

            if is_tabu:
                # Apply aspiration criteria
                if aspiration_function(
                    neighbor_cost, current_cost, best_cost, iteration, max_iterations
                ):
                    if debug:
                        print(f"Accepting tabu move {move} due to aspiration criteria")
                    aspiration_acceptances += 1
                else:
                    continue

            # Accept the neighbor if it's better than the current best neighbor
            if neighbor_cost < best_neighbor_cost:
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
        print(f"Aspiration acceptances: {aspiration_acceptances}")

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
        "--tabu-size",
        type=int,
        default=None,
        help="Size of the tabu list (if not specified, will be calculated dynamically)",
    )
    parser.add_argument(
        "--neighborhood-size",
        type=int,
        default=20,
        help="Number of neighbors to evaluate in each iteration",
    )
    parser.add_argument(
        "--sampling-strategy",
        choices=["vertex", "edge", "edge_vertex"],
        default="vertex",
        help="Strategy for generating neighbors: vertex, edge, or edge_vertex",
    )

    args = parser.parse_args()

    # Map 'p' criteria to 's' for the when_to_ride function
    search_criteria = args.method

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
        sampling_strategy=args.sampling_strategy,
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
