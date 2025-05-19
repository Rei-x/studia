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
    total_path = []
    current_time = get_time_in_seconds(start_time)
    current_station = start_station
    total_transfers = 0

    complete_sequence = station_sequence.copy()

    if debug:
        print(f"Evaluating sequence: {complete_sequence}")

    for next_station in complete_sequence:
        if debug:
            print(
                f"Finding route from {current_station} to {next_station} at {format_time(current_time)}"
            )

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

        if debug:
            print(f"Route found, arrival time: {format_time(arrival_time)}")

        current_time = arrival_time
        current_station = next_station
        total_path.extend(path)

        if criteria == "s" or criteria == "p":
            segment_transfers = len(set(ride[0] for ride in path)) - 1
            total_transfers += segment_transfers

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

    if criteria == "t":
        total_cost = arrival_time - get_time_in_seconds(start_time)
    else:
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
    if not stations_to_visit:
        return 0, []

    current_sequence = stations_to_visit.copy()
    random.shuffle(current_sequence)

    if debug:
        print(f"Initial sequence: {current_sequence}")

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
            return inf, []

    best_sequence = current_sequence.copy()
    best_cost = current_cost
    best_path = current_path

    if debug:
        print(f"Initial cost: {best_cost}")

    tabu_list = []

    for iteration in range(max_iterations):
        if debug:
            print(f"\nIteration {iteration + 1}/{max_iterations}")
            print(f"Current sequence: {current_sequence}")
            print(f"Current cost: {current_cost}")

        best_neighbor_cost = inf
        best_neighbor_sequence = None
        best_neighbor_path = []

        for _ in range(
            min(
                neighborhood_size,
                len(current_sequence) * (len(current_sequence) - 1) // 2,
            )
        ):
            move_type = random.choice(["swap", "insert"])

            if move_type == "swap" and len(current_sequence) >= 2:
                i, j = random.sample(range(len(current_sequence)), 2)
                neighbor_sequence = current_sequence.copy()
                neighbor_sequence[i], neighbor_sequence[j] = (
                    neighbor_sequence[j],
                    neighbor_sequence[i],
                )
                move = ("swap", i, j)
            elif move_type == "insert" and len(current_sequence) >= 2:
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

            if move in tabu_list:
                if best_cost < inf:
                    neighbor_cost, neighbor_path, is_valid = calculate_route_cost(
                        start_station,
                        neighbor_sequence,
                        criteria,
                        start_time,
                        graph,
                        station_coordinates,
                        debug=False,
                    )

                    if is_valid and neighbor_cost < best_cost:
                        if debug:
                            print(
                                f"Accepting tabu move {move} due to aspiration criteria"
                            )
                        best_neighbor_cost = neighbor_cost
                        best_neighbor_sequence = neighbor_sequence
                        best_neighbor_path = neighbor_path
                        break
                continue

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
            current_sequence = best_neighbor_sequence
            current_cost = best_neighbor_cost
            current_path = best_neighbor_path

            tabu_list.append(best_neighbor_move)
            if len(tabu_list) > tabu_size:
                tabu_list.pop(0)

            if debug:
                print(f"Moving to neighbor with cost {current_cost}")

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

    search_criteria = args.method

    df = load_data()
    graph, station_coordinates = build_graph(df)

    start_timer = time.time()

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

    end_timer = time.time()
    computation_time = end_timer - start_timer

    if best_cost == inf or not best_path:
        print("No valid route found")
        print("Cost: inf", file=sys.stderr)
    else:
        for ride in best_path:
            line_name, board_stop, board_time, alight_stop, alight_time = ride
            formatted_board_time = format_time(board_time)
            formatted_alight_time = format_time(alight_time)
            print(
                f"{line_name}, {formatted_board_time}, {board_stop}, {formatted_alight_time}, {alight_stop}"
            )

        print(f"Cost: {best_cost}", file=sys.stderr)

    print(f"Computation time: {computation_time:.2f} seconds", file=sys.stderr)


if __name__ == "__main__":
    main()
