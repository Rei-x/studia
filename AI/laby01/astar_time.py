import pandas as pd
from math import inf, cos, sqrt, radians
import heapq
import time
import sys


df = pd.read_csv("connection_graph.csv")

all_stations = pd.concat([df["start_stop"], df["end_stop"]])
unique_stations = all_stations.unique()
unique_stations.sort()

# Create a dictionary to store station coordinates
station_coordinates = {}
for row in unique_stations:
    if row not in station_coordinates:
        start_entries = df[df["start_stop"] == row]
        end_entries = df[df["end_stop"] == row]

        if not start_entries.empty:
            first_station = start_entries.iloc[0]
            station_coordinates[row] = (
                first_station["start_stop_lat"],
                first_station["start_stop_lon"],
            )
        elif not end_entries.empty:
            first_station = end_entries.iloc[0]
            station_coordinates[row] = (
                first_station["end_stop_lat"],
                first_station["end_stop_lon"],
            )


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


def heuristic(start_station, end_station):
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
    avg_speed = 8.33  # meters per second

    # Estimated travel time in seconds
    estimated_time = distance / avg_speed

    return estimated_time


def when_to_ride(start_station, end_station, criteria, start_time):
    nodes = {station: inf for station in unique_stations}
    start_seconds = get_time_in_seconds(start_time)

    nodes[start_station] = start_seconds

    print(
        f"Starting at station {start_station} at {start_time} ({nodes[start_station]} seconds)"
    )

    prev = {}  # Maps station -> (previous_station, (line, board_stop, board_time, alight_stop, alight_time))
    visited = set()
    pq = []

    # Add heuristic to the priority queue
    h_value = heuristic(start_station, end_station)
    heapq.heappush(
        pq, (nodes[start_station] + h_value, nodes[start_station], start_station)
    )

    while pq:
        _, current_time, current_node = heapq.heappop(pq)
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
        neighbors = df[df["start_stop"] == current_node]

        for _idx, row in neighbors.iterrows():
            neighbor = row["end_stop"]
            if neighbor in visited:
                continue

            sched_departure = get_time_in_seconds(row["departure_time"])
            current_day_time = current_time % 86400
            day_start = current_time - current_day_time
            if sched_departure < current_day_time:
                abs_departure = day_start + sched_departure + 86400
            else:
                abs_departure = day_start + sched_departure

            ride_duration = get_time_difference(
                get_time_in_seconds(row["departure_time"]),
                get_time_in_seconds(row["arrival_time"]),
            )
            new_time = abs_departure + ride_duration

            if new_time < nodes[neighbor]:
                nodes[neighbor] = new_time
                prev[neighbor] = (
                    current_node,
                    (row["line"], current_node, abs_departure, neighbor, new_time),
                )
                # Add heuristic to priority
                h_value = heuristic(neighbor, end_station)
                heapq.heappush(pq, (new_time + h_value, new_time, neighbor))

    print("No route found")
    return inf, []


start_comp = time.time()
result_time, path = when_to_ride("Śliczna", "most Grunwaldzki", "t", "08:50:00")
end_comp = time.time()

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
