import pandas as pd
from math import inf, cos, sqrt, radians
import heapq

from utils import get_time_difference, get_time_in_seconds


def load_data(file_path="connection_graph.csv"):
    """Load connection data from CSV file."""
    return pd.read_csv(file_path)


def pythagorean_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the approximate distance between two points using Pythagorean theorem.
    This is a simplification that works well for small distances.
    """
    # Convert latitude difference to approximate distance in meters
    # 1 degree of latitude is approximately 111,000 meters
    y = (lat2 - lat1) * 111000

    # Convert longitude difference to approximate distance in meters
    # 1 degree of longitude is approximately 111,000 * cos(latitude) meters
    # Using the average latitude for the calculation
    avg_lat_radians = radians((lat1 + lat2) / 2)
    x = (lon2 - lon1) * 111000 * cos(avg_lat_radians)

    # Calculate Euclidean distance using Pythagorean theorem
    return sqrt(x * x + y * y)


def heuristic(start_station, end_station, station_coordinates):
    """Calculate the estimated travel time based on geographical distance."""
    if (
        start_station not in station_coordinates
        or end_station not in station_coordinates
    ):
        raise ValueError(
            f"Station coordinates not found for {start_station} or {end_station}"
        )

    start_lat, start_lon = station_coordinates[start_station]
    end_lat, end_lon = station_coordinates[end_station]

    # Calculate distance in meters using Pythagorean theorem
    distance = pythagorean_distance(start_lat, start_lon, end_lat, end_lon)

    # Assume an average speed of 30 km/h (8.33 m/s) for public transport
    avg_speed = 30 * (10 / 36)  # meters per second

    # Estimated travel time in seconds
    estimated_time = distance / avg_speed

    return estimated_time


def build_graph(df):
    """
    Builds a graph representation from the connections DataFrame and extracts station information.

    Args:
        df: DataFrame with connection data

    Returns:
        Tuple of (graph, station_coordinates, all_stations)
        - graph: Dictionary where keys are station names and values are lists of outgoing connections
        - station_coordinates: Dictionary of station coordinates
        - all_stations: List of all unique station names
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


def when_to_ride(
    start_station,
    end_station,
    criteria,
    start_time,
    debug=False,
    graph=None,
    station_coordinates=None,
    df=None,
):
    """
    Find the optimal route from start_station to end_station.

    Args:
        start_station: Name of the starting station
        end_station: Name of the destination station
        criteria: Criteria for optimization ('t' for time, 'p' for transfers)
        start_time: Starting time in "HH:MM:SS" format
        df: Optional DataFrame with connection data
        debug: Whether to print debug information

    Returns:
        Tuple of (arrival_time, path)
    """
    # Load data if not provided
    if graph is None:
        df = load_data()
        # Build the graph representation and get station information
        graph, station_coordinates = build_graph(df)

    all_stations = sorted(list(graph.keys()))

    # Check if start and end stations exist
    if start_station not in graph or end_station not in graph:
        if debug:
            print(
                f"Station not found: {start_station if start_station not in graph else end_station}"
            )
        return inf, []

    # We now store nodes differently based on criteria
    # For time optimization: {station: (time, transfers)}
    # For transfers optimization: {station: (transfers, time)}
    nodes = {}
    start_seconds = get_time_in_seconds(start_time)

    for station in all_stations:
        if criteria == "t":
            nodes[station] = (inf, inf)  # (time, transfers) for time optimization
        else:  # criteria == 'p'
            nodes[station] = (inf, inf)  # (transfers, time) for transfers optimization

    # Initialize starting node
    if criteria == "t":
        nodes[start_station] = (start_seconds, 0)  # (time, transfers)
    else:  # criteria == 'p'
        nodes[start_station] = (0, start_seconds)  # (transfers, time)

    if debug:
        print(
            f"Starting at station {start_station} at {start_time} ({start_seconds} seconds)"
        )

    # Maps station -> (previous_station, current_line, (line, board_stop, board_time, alight_stop, alight_time))
    prev = {}
    visited = set()
    pq = []

    # Calculate heuristic safely
    try:
        time_heuristic = heuristic(start_station, end_station, station_coordinates)
    except ValueError:
        # If heuristic calculation fails, use a default value
        time_heuristic = 0

    # Initial priority queue entry based on criteria
    if criteria == "t":
        # Prioritize time
        heapq.heappush(
            pq, (start_seconds + time_heuristic, 0, start_seconds, start_station, None)
        )
    else:  # criteria == 'p'
        # Prioritize transfers
        heapq.heappush(
            pq, (0, start_seconds + time_heuristic, start_seconds, start_station, None)
        )

    while pq:
        if criteria == "t":
            # Prioritize time
            _, transfers, current_time, current_node, current_line = heapq.heappop(pq)
        else:  # criteria == 'p'
            # Prioritize transfers
            transfers, _, current_time, current_node, current_line = heapq.heappop(pq)

        # Skip if we've found a better path already - comparison depends on criteria
        if criteria == "t":
            # For time optimization, compare (time, transfers)
            if (current_time, transfers) > nodes[current_node]:
                continue
        else:  # criteria == 'p'
            # For transfers optimization, compare (transfers, time)
            if (transfers, current_time) > nodes[current_node]:
                continue

        if current_node == end_station:
            path = []
            node = end_station
            while node in prev:
                prev_node, prev_line, ride = prev[node]
                path.append(ride)
                node = prev_node
            path.reverse()
            if debug:
                print("Found final node")
            return current_time, path

        # Only mark as visited after we've processed the node
        visited.add(current_node)

        # Get neighbors from the graph instead of filtering the DataFrame
        for connection in graph.get(current_node, []):
            neighbor = connection["end_stop"]
            if neighbor in visited:
                continue

            # Calculate new transfer count - increment if line changes
            new_line = connection["line"]
            new_transfers = transfers
            if current_line is not None and new_line != current_line:
                new_transfers += 1

            sched_departure = connection["departure_seconds"]
            current_day_time = current_time % 86400
            day_start = current_time - current_day_time
            if sched_departure < current_day_time:
                abs_departure = day_start + sched_departure + 86400
            else:
                abs_departure = day_start + sched_departure

            ride_duration = get_time_difference(
                sched_departure, connection["arrival_seconds"]
            )
            new_time = abs_departure + ride_duration

            if criteria == "t":
                # For time optimization, compare (time, transfers)
                if (new_time, new_transfers) < nodes[neighbor]:
                    nodes[neighbor] = (new_time, new_transfers)
                    prev[neighbor] = (
                        current_node,
                        new_line,
                        (new_line, current_node, abs_departure, neighbor, new_time),
                    )

                    # Calculate heuristic
                    try:
                        time_heuristic = heuristic(
                            neighbor, end_station, station_coordinates
                        )
                    except ValueError:
                        time_heuristic = 0

                    # Priority queue entry for time optimization
                    heapq.heappush(
                        pq,
                        (
                            new_time + time_heuristic,  # F = g + h based on time
                            new_transfers,
                            new_time,
                            neighbor,
                            new_line,
                        ),
                    )
            else:  # criteria == 's'
                # For transfers optimization, compare (transfers, time)
                if (new_transfers, new_time) < nodes[neighbor]:
                    nodes[neighbor] = (new_transfers, new_time)
                    prev[neighbor] = (
                        current_node,
                        new_line,
                        (new_line, current_node, abs_departure, neighbor, new_time),
                    )

                    # Calculate heuristic
                    try:
                        time_heuristic = heuristic(
                            neighbor, end_station, station_coordinates
                        )
                    except ValueError:
                        time_heuristic = 0

                    # Priority queue entry for transfers optimization
                    heapq.heappush(
                        pq,
                        (
                            new_transfers,  # F based on transfers
                            new_time + time_heuristic,
                            new_time,
                            neighbor,
                            new_line,
                        ),
                    )

    if debug:
        print("No route found")
    return inf, []
