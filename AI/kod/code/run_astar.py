import argparse
from math import inf
import sys
import time
from astar_time_przesiadki import build_graph, load_data, when_to_ride
from utils import format_time


def print_travel_schedule(result_time, path):
    """Print the travel schedule in a human-readable format."""
    if result_time == inf:
        print("No route found")
        return

    print("\nTravel Schedule:")
    current_line = None
    segment_start_station = None
    segment_start_time = None
    previous_ride_end_station = None
    previous_ride_end_time = None

    for ride in path:
        line = ride[0]
        if line != current_line:
            if current_line is not None:
                print(
                    f"Linia {current_line}, wsiadam: {segment_start_time} {segment_start_station}, wsiadam: {previous_ride_end_time} {previous_ride_end_station}"
                )
            current_line = line
            segment_start_station = ride[1]
            segment_start_time = format_time(ride[2])
        previous_ride_end_station = ride[3]
        previous_ride_end_time = format_time(ride[4])

    if current_line is not None:
        print(
            f"Linia {current_line}, wsiadam: {segment_start_time} {segment_start_station}, wsiadam: {previous_ride_end_time} {previous_ride_end_station}"
        )

    print("\nEarliest arrival time:", format_time(int(result_time)))


def main(
    start_station="Śliczna",
    end_station="most Grunwaldzki",
    start_time="08:50:00",
    criteria="t",
    data_file="connection_graph.csv",
):
    """Main function to run the A* algorithm and print results."""

    df = load_data(data_file)
    graph, stations = build_graph(df)
    start_comp = time.time()
    result_time, path = when_to_ride(
        start_station,
        end_station,
        criteria,
        start_time,
        graph=graph,
        station_coordinates=stations,
        debug=True,
    )
    end_comp = time.time()

    print_travel_schedule(result_time, path)

    comp_time = end_comp - start_comp
    sys.stderr.write(
        f"Cost: {result_time} seconds; Computation time: {comp_time:.4f} seconds\n"
    )

    return result_time, path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Find optimal routes using A* algorithm"
    )
    parser.add_argument("--start", default="Śliczna", help="Starting station")
    parser.add_argument("--end", default="most Grunwaldzki", help="Destination station")
    parser.add_argument(
        "--method",
        default="t",
        choices=["t", "p"],
        help="Method: 't' for time optimization, 'p' for transfers optimization",
    )
    parser.add_argument("--time", default="08:50:00", help="Start time (HH:MM:SS)")
    parser.add_argument("--data", default="connection_graph.csv", help="Data file path")

    args = parser.parse_args()

    main(args.start, args.end, args.time, args.method, args.data)
