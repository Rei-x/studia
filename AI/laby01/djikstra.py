import pandas as pd
from math import inf
import heapq
import time
import sys


df = pd.read_csv("connection_graph.csv")

all_stations = pd.concat([df["start_stop"], df["end_stop"]])
unique_stations = all_stations.unique()
unique_stations.sort()


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


def when_to_ride(start_station, end_station, criteria, start_time):
    nodes = {station: inf for station in unique_stations}

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

        # print(f"Checking node {current_node} at time {format_time(current_time)}")
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
        # print(f"Found {len(neighbors)} neighbors for {current_node}")

        for _idx, row in neighbors.iterrows():
            neighbor = row["end_stop"]
            if neighbor in visited:
                continue

            sched_departure = get_time_in_seconds(row["departure_time"])

            if sched_departure < current_time:
                sched_departure += 86400

            ride_duration = get_time_difference(
                get_time_in_seconds(row["departure_time"]),
                get_time_in_seconds(row["arrival_time"]),
            )
            # jesteśmy o 9:00 na przystanku śliczna
            # odjeżdżamy o 9:10, przyjeżdżamy o 9:30
            # current_time = 9:00
            # sched_departure = 9:10
            # ride_duration = 20
            # full cost = 9:10 + 20 = 9:30
            new_time = sched_departure + ride_duration

            if new_time < nodes[neighbor]:
                print(
                    "new best for ",
                    neighbor,
                    ":",
                    format_time(new_time),
                    " via ",
                    row["line"],
                )
                nodes[neighbor] = new_time
                prev[neighbor] = (
                    current_node,
                    (row["line"], current_node, sched_departure, neighbor, new_time),
                )
                heapq.heappush(pq, (new_time, neighbor))

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
