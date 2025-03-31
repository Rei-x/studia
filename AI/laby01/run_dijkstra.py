import argparse
import time
import sys
from djikstra import load_data, build_graph, when_to_ride, format_time


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Find optimal route using Dijkstra's algorithm"
    )
    parser.add_argument("--start", required=True, help="Starting station")
    parser.add_argument("--end", required=True, help="Destination station")
    parser.add_argument(
        "--method",
        choices=["t", "s"],
        default="t",
        help="Optimization criteria: t for time, s for transfers",
    )
    parser.add_argument(
        "--time", required=True, help="Starting time in HH:MM:SS format"
    )

    args = parser.parse_args()

    # Load data and build graph (not included in timing)
    df = load_data()
    graph, _ = build_graph(df)

    # Start timing only for the algorithm execution
    start_comp = time.time()
    result_time, path = when_to_ride(
        args.start, args.end, args.method, args.time, graph=graph
    )
    end_comp = time.time()

    # Output results
    if result_time == float("inf"):
        print("No route found")
    else:
        print("\nTravel Schedule:")
        current_line = None
        segment_start_station = None
        segment_start_time = None
        previous_ride_end_station = None
        previous_ride_end_time = None

        for ride in path:
            line = ride[0]
            if line != current_line:
                # print previous line segment if any
                if current_line is not None:
                    print(
                        f"Linia {current_line}, wsiadam: {segment_start_time} {segment_start_station}, wysiadam: {previous_ride_end_time} {previous_ride_end_station}"
                    )
                current_line = line
                segment_start_station = ride[1]
                segment_start_time = format_time(ride[2])
            previous_ride_end_station = ride[3]
            previous_ride_end_time = format_time(ride[4])

        # print the final segment
        if current_line is not None:
            print(
                f"Linia {current_line}, wsiadam: {segment_start_time} {segment_start_station}, wysiadam: {previous_ride_end_time} {previous_ride_end_station}"
            )

        print("\nEarliest arrival time:", format_time(int(result_time)))

    comp_time = end_comp - start_comp
    print(
        f"Cost: {result_time} seconds; Computation time: {comp_time:.4f} seconds",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
