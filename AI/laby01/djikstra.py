import pandas as pd
from math import inf
import heapq
import time
import sys


def get_time_in_seconds(time_str: str):
    hours, minutes, seconds = time_str.split(":")
    return int(hours) * 3600 + int(minutes) * 60 + int(seconds)


def get_time_difference(departure: int, arrive: int):
    if departure > arrive:
        arrive += 3600 * 24
    return arrive - departure


def format_time(seconds: int):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{secs:02}"


def load_data(file_path="connection_graph.csv"):
    """Load connection data from CSV file."""
    return pd.read_csv(file_path)


def build_graph(df):
    """
    Builds a graph representation from the connections DataFrame.

    Args:
        df: DataFrame with connection data

    Returns:
        Tuple of (graph, station_coordinates)
        - graph: Dictionary where keys are station names and values are lists of outgoing connections
        - station_coordinates: Dictionary of station coordinates
    """
    graph = {}
    station_coordinates = {}

    # Process all start stations
    for start_station, group in df.groupby("start_stop"):
        if start_station not in graph:
            graph[start_station] = []

        # Get the first row to extract start station coordinates
        first_row = group.iloc[0]
        station_coordinates[start_station] = (
            first_row["start_stop_lat"],
            first_row["start_stop_lon"],
        )

        # Add all outgoing connections for this station
        for _, row in group.iterrows():
            connection = {
                "end_stop": row["end_stop"],
                "line": row["line"],
                "departure_time": row["departure_time"],
                "arrival_time": row["arrival_time"],
                "departure_seconds": get_time_in_seconds(row["departure_time"]),
                "arrival_seconds": get_time_in_seconds(row["arrival_time"]),
            }
            graph[start_station].append(connection)

            # Add end station coordinates if not already present
            if row["end_stop"] not in station_coordinates:
                station_coordinates[row["end_stop"]] = (
                    row["end_stop_lat"],
                    row["end_stop_lon"],
                )

    # Make sure all end stations are in the graph (even if they have no outgoing connections)
    for end_station in df["end_stop"].unique():
        if end_station not in graph:
            graph[end_station] = []

    return graph, station_coordinates


def when_to_ride(start_station, end_station, criteria, start_time, graph=None, df=None):
    """
    Find the optimal route from start_station to end_station using Dijkstra's algorithm.

    Args:
        start_station: Name of the starting station
        end_station: Name of the destination station
        criteria: Criteria for optimization ('t' for time, 's' for transfers)
        start_time: Starting time in "HH:MM:SS" format
        graph: Pre-built graph (if None, will build from df)
        df: DataFrame with connection data (if graph is None)

    Returns:
        Tuple of (arrival_time, path)
    """
    # Load data if not provided
    if graph is None and df is None:
        df = load_data()
        # Build the graph representation
        graph, _ = build_graph(df)

    # Get all unique stations
    all_stations = sorted(list(graph.keys()))

    # Check if start and end stations exist
    if start_station not in graph or end_station not in graph:
        print(
            f"Station not found: {start_station if start_station not in graph else end_station}"
        )
        return inf, []

    # Initialize distances
    nodes = {station: inf for station in all_stations}
    nodes[start_station] = get_time_in_seconds(start_time)

    print(
        f"Starting at station {start_station} at {start_time} ({nodes[start_station]} seconds)"
    )

    prev = {}  # Maps station -> (previous_station, (line, board_stop, board_time, alight_stop, alight_time))
    visited = set()
    pq = []

    heapq.heappush(pq, (nodes[start_station], start_station))

    while pq:
        current_time, current_node = heapq.heappop(pq)

        if current_time > nodes[current_node]:
            continue

        if current_node == end_station:
            path = []
            node = end_station
            while node in prev:
                ride = prev[node][1]
                path.append(ride)
                node = prev[node][0]
            path.reverse()
            print("Found final node")
            return current_time, path

        visited.add(current_node)

        # Process all connections from current node
        for connection in graph.get(current_node, []):
            neighbor = connection["end_stop"]
            if neighbor in visited:
                continue

            sched_departure = connection["departure_seconds"]

            # Handle day cycling (if departure is before current time, add a day)
            if sched_departure < current_time % 86400:
                sched_departure += 86400

            # Adjust departure to absolute time
            current_day_time = current_time % 86400
            day_start = current_time - current_day_time

            if sched_departure < current_day_time:
                abs_departure = day_start + sched_departure + 86400
            else:
                abs_departure = day_start + sched_departure

            ride_duration = get_time_difference(
                connection["departure_seconds"], connection["arrival_seconds"]
            )
            new_time = abs_departure + ride_duration

            if new_time < nodes[neighbor]:
                nodes[neighbor] = new_time
                prev[neighbor] = (
                    current_node,
                    (
                        connection["line"],
                        current_node,
                        abs_departure,
                        neighbor,
                        new_time,
                    ),
                )
                heapq.heappush(pq, (new_time, neighbor))

    print("No route found")
    return inf, []


def main():
    # Load data and build graph first (not included in computation time)
    df = load_data()
    graph, _ = build_graph(df)

    # Define route
    start_station = "Śliczna"
    end_station = "Bezpieczna"  # Change this to test different scenarios
    criteria = "t"
    start_time = "16:25:00"

    # Start timing only for the route finding algorithm
    start_comp = time.time()
    result_time, path = when_to_ride(
        start_station, end_station, criteria, start_time, graph=graph
    )
    end_comp = time.time()

    # Output results
    if result_time == inf:
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
    sys.stderr.write(
        f"Cost: {result_time} seconds; Computation time: {comp_time:.4f} seconds\n"
    )


if __name__ == "__main__":
    main()
