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


def heuristic(pos_0, pos_1):
    start_lat, start_lon = pos_0
    end_lat, end_lon = pos_1

    # Calculate distance in meters using Pythagorean theorem
    distance = pythagorean_distance(start_lat, start_lon, end_lat, end_lon)

    # Assume an average speed of 30 km/h (8.33 m/s) for public transport
    avg_speed = 30 * (10 / 36)  # meters per second

    # Estimated travel time in seconds
    estimated_time = distance / avg_speed

    return estimated_time


class Node:
    def __init__(self, station: str, lat: float, lon: float):
        self.station = station
        self.lat = lat
        self.lon = lon
        self.connections = []
        self.time = inf
        self.transfers = inf
        self.heuristic = inf

    def add_connection(self, connection):
        self.connections.append(connection)

    def time_score(self):
        return self.time + self.heuristic if self.heuristic else self.time

    def transfer_score(self):
        return self.transfers + self.heuristic if self.heuristic else self.transfers


class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node):
        self.nodes[node.station] = node

    def get_node(self, name) -> Node:
        node = self.nodes.get(name)

        if node is None:
            raise ValueError(f"Node {name} not found in graph")

        return node

    def has_node(self, name):
        return name in self.nodes

    def __repr__(self):
        return f"Graph({len(self.nodes)} nodes)"

    def __getitem__(self, item):
        if item not in self.nodes:
            raise KeyError(f"Node {item} not found in graph")
        return self.nodes[item].connections

    def __contains__(self, item):
        return item in self.nodes

    def __len__(self):
        return len(self.nodes)


def build_graph(df):
    graph = Graph()

    for _, row in df.iterrows():
        start_node = Node(
            row["start_stop"],
            row["start_stop_lat"],
            row["start_stop_lon"],
        )
        end_node = Node(
            row["end_stop"],
            row["end_stop_lat"],
            row["end_stop_lon"],
        )

        departure_seconds = get_time_in_seconds(row["departure_time"])
        arrival_seconds = get_time_in_seconds(row["arrival_time"])

        connection = {
            "end_stop": row["end_stop"],
            "line": row["line"],
            "departure_time": row["departure_time"],
            "arrival_time": row["arrival_time"],
            "node": end_node,
            "departure_seconds": departure_seconds,
            "arrival_seconds": arrival_seconds,
            "travel_time": get_time_difference(departure_seconds, arrival_seconds),
        }

        start_node.add_connection(connection)

        graph.add_node(start_node)
        graph.add_node(end_node)

    return graph


def when_to_ride(
    start_station, end_station, criteria, start_time, debug=False, graph=None
):
    """
    Find the optimal route from start_station to end_station.

    Args:
        start_station: Name of the starting station
        end_station: Name of the destination station
        criteria: Criteria for optimization ('t' for time, 's' for transfers)
        start_time: Starting time in "HH:MM:SS" format
        graph: Optional Graph object with connection data
        debug: Whether to print debug information

    Returns:
        Tuple of (arrival_time, path)
    """
    # Load data if not provided
    if graph is None:
        df = load_data()
        # Build the graph representation and get station information
        graph = build_graph(df)

    # Check if start and end stations exist
    if not graph.has_node(start_station) or not graph.has_node(end_station):
        if debug:
            print(
                f"Station not found: {start_station if not graph.has_node(start_station) else end_station}"
            )
        return inf, []

    start_seconds = get_time_in_seconds(start_time)

    # Reset all nodes
    for _station_name, node in graph.nodes.items():
        node.time = inf
        node.transfers = inf
        node.heuristic = 0

    start_node = graph.get_node(start_station)
    end_node = graph.get_node(end_station)
    start_node.time = start_seconds
    start_node.transfers = 0

    start_node.heuristic = heuristic(
        (start_node.lat, start_node.lon), (end_node.lat, end_node.lon)
    )

    if debug:
        print(
            f"Starting at station {start_station} at {start_time} ({start_seconds} seconds)"
        )

    # Maps station -> (previous_station, current_line, (line, board_stop, board_time, alight_stop, alight_time))
    prev = {}
    visited = set()
    pq = []

    # Initial priority queue entry based on criteria
    if criteria == "t":
        # Prioritize time
        heapq.heappush(
            pq, (start_node.time_score(), 0, start_seconds, start_station, None)
        )
    else:  # criteria == 's'
        # Prioritize transfers
        heapq.heappush(
            pq, (0, start_node.time_score(), start_seconds, start_station, None)
        )

    while pq:
        if criteria == "t":
            # Prioritize time
            _, transfers, current_time, current_station, current_line = heapq.heappop(
                pq
            )
        else:  # criteria == 's'
            # Prioritize transfers
            transfers, _, current_time, current_station, current_line = heapq.heappop(
                pq
            )

        current_node = graph.get_node(current_station)

        # Skip if we've found a better path already
        if criteria == "t" and current_time > current_node.time:
            continue
        elif criteria == "s" and transfers > current_node.transfers:
            continue

        if current_station == end_station:
            path = []
            station = end_station
            while station in prev:
                prev_station, prev_line, ride = prev[station]
                path.append(ride)
                station = prev_station
            path.reverse()
            if debug:
                print("Found final node")
            return current_time, path

        # Only mark as visited after we've processed the node
        visited.add(current_station)

        # Process neighbors using node connections
        for connection in current_node.connections:
            neighbor_station = connection["end_stop"]
            if neighbor_station in visited:
                continue

            neighbor_node = graph.get_node(neighbor_station)

            # Calculate new transfer count - increment if line changes
            new_line = connection["line"]
            new_transfers = transfers
            if current_line is not None and new_line != current_line:
                new_transfers += 1

            sched_departure = get_time_in_seconds(connection["departure_time"])

            if sched_departure < current_time:
                sched_departure += 86400

            ride_duration = connection["travel_time"]
            new_time = sched_departure + ride_duration

            if criteria == "t":
                # For time optimization
                if new_time < neighbor_node.time:
                    neighbor_node.time = new_time
                    neighbor_node.transfers = new_transfers
                    neighbor_node.heuristic = heuristic(
                        (neighbor_node.lat, neighbor_node.lon),
                        (end_node.lat, end_node.lon),
                    )

                    prev[neighbor_station] = (
                        current_station,
                        new_line,
                        (
                            new_line,
                            current_station,
                            sched_departure,
                            neighbor_station,
                            new_time,
                        ),
                    )

                    # Priority queue entry for time optimization
                    heapq.heappush(
                        pq,
                        (
                            neighbor_node.time_score(),
                            new_transfers,
                            new_time,
                            neighbor_station,
                            new_line,
                        ),
                    )
            else:  # criteria == 's'
                # For transfers optimization
                if new_transfers < neighbor_node.transfers or (
                    new_transfers == neighbor_node.transfers
                    and new_time < neighbor_node.time
                ):
                    neighbor_node.time = new_time
                    neighbor_node.transfers = new_transfers
                    neighbor_node.heuristic = heuristic(
                        (neighbor_node.lat, neighbor_node.lon),
                        (end_node.lat, end_node.lon),
                    )

                    prev[neighbor_station] = (
                        current_station,
                        new_line,
                        (
                            new_line,
                            current_station,
                            sched_departure,
                            neighbor_station,
                            new_time,
                        ),
                    )

                    # Priority queue entry for transfers optimization
                    heapq.heappush(
                        pq,
                        (
                            new_transfers,
                            neighbor_node.time_score(),
                            new_time,
                            neighbor_station,
                            new_line,
                        ),
                    )

    if debug:
        print("No route found")
    return inf, []
