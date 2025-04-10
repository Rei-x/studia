import pandas as pd
from math import inf, cos, sqrt, radians
import heapq

from utils import get_time_difference, get_time_in_seconds


def load_data(file_path="connection_graph.csv"):
    return pd.read_csv(file_path)


def pythagorean_distance(lat1, lon1, lat2, lon2):
    y = (lat2 - lat1) * 111000

    avg_lat_radians = radians((lat1 + lat2) / 2)
    x = (lon2 - lon1) * 111000 * cos(avg_lat_radians)

    return sqrt(x * x + y * y)


def heuristic(start_station, end_station, station_coordinates):
    if (
        start_station not in station_coordinates
        or end_station not in station_coordinates
    ):
        raise ValueError(
            f"Station coordinates not found for {start_station} or {end_station}"
        )

    start_lat, start_lon = station_coordinates[start_station]
    end_lat, end_lon = station_coordinates[end_station]

    distance = pythagorean_distance(start_lat, start_lon, end_lat, end_lon)

    avg_speed = 30 * (10 / 36)

    estimated_time = distance / avg_speed

    return estimated_time


def build_graph(df):
    graph = {}
    station_coordinates = {}

    for start_station, group in df.groupby("start_stop"):
        if start_station not in graph:
            graph[start_station] = []

        first_row = group.iloc[0]
        station_coordinates[start_station] = (
            first_row["start_stop_lat"],
            first_row["start_stop_lon"],
        )

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

            if row["end_stop"] not in station_coordinates:
                station_coordinates[row["end_stop"]] = (
                    row["end_stop_lat"],
                    row["end_stop_lon"],
                )

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
    if graph is None:
        df = load_data()

        graph, station_coordinates = build_graph(df)

    all_stations = sorted(list(graph.keys()))

    if start_station not in graph or end_station not in graph:
        if debug:
            print(
                f"Station not found: {start_station if start_station not in graph else end_station}"
            )
        return inf, []

    nodes = {}
    start_seconds = get_time_in_seconds(start_time)

    for station in all_stations:
        if criteria == "t":
            nodes[station] = (inf, inf)
        else:
            nodes[station] = (inf, inf)

    if criteria == "t":
        nodes[start_station] = (start_seconds, 0)
    else:
        nodes[start_station] = (0, start_seconds)

    if debug:
        print(
            f"Starting at station {start_station} at {start_time} ({start_seconds} seconds)"
        )

    prev = {}
    visited = set()
    pq = []

    try:
        time_heuristic = heuristic(start_station, end_station, station_coordinates)
    except ValueError:
        time_heuristic = 0

    if criteria == "t":
        heapq.heappush(
            pq, (start_seconds + time_heuristic, 0, start_seconds, start_station, None)
        )
    else:
        heapq.heappush(
            pq, (0, start_seconds + time_heuristic, start_seconds, start_station, None)
        )

    while pq:
        if criteria == "t":
            _, transfers, current_time, current_node, current_line = heapq.heappop(pq)
        else:
            transfers, _, current_time, current_node, current_line = heapq.heappop(pq)

        if criteria == "t":
            if (current_time, transfers) > nodes[current_node]:
                continue
        else:
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

        visited.add(current_node)

        for connection in graph.get(current_node, []):
            neighbor = connection["end_stop"]
            if neighbor in visited:
                continue

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
                if (new_time, new_transfers) < nodes[neighbor]:
                    nodes[neighbor] = (new_time, new_transfers)
                    prev[neighbor] = (
                        current_node,
                        new_line,
                        (new_line, current_node, abs_departure, neighbor, new_time),
                    )

                    try:
                        time_heuristic = heuristic(
                            neighbor, end_station, station_coordinates
                        )
                    except ValueError:
                        time_heuristic = 0

                    heapq.heappush(
                        pq,
                        (
                            new_time + time_heuristic,
                            new_transfers,
                            new_time,
                            neighbor,
                            new_line,
                        ),
                    )
            else:
                if (new_transfers, new_time) < nodes[neighbor]:
                    nodes[neighbor] = (new_transfers, new_time)
                    prev[neighbor] = (
                        current_node,
                        new_line,
                        (new_line, current_node, abs_departure, neighbor, new_time),
                    )

                    try:
                        time_heuristic = heuristic(
                            neighbor, end_station, station_coordinates
                        )
                    except ValueError:
                        time_heuristic = 0

                    heapq.heappush(
                        pq,
                        (
                            new_transfers,
                            new_time + time_heuristic,
                            new_time,
                            neighbor,
                            new_line,
                        ),
                    )

    if debug:
        print("No route found")
    return inf, []
