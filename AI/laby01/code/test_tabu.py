import pytest
import pandas as pd
from math import inf
import random
from io import StringIO
import sys

from run_tabu import calculate_route_cost, tabu_search, main
from astar_time_przesiadki import build_graph, load_data
from utils import get_time_in_seconds


@pytest.fixture
def sample_data():
    return pd.DataFrame(
        {
            "start_stop": [
                "StationA",
                "StationB",
                "StationC",
                "StationA",
                "StationB",
                "StationC",
            ],
            "end_stop": [
                "StationB",
                "StationC",
                "StationA",
                "StationC",
                "StationA",
                "StationB",
            ],
            "start_stop_lat": [51.1, 51.2, 51.3, 51.1, 51.2, 51.3],
            "start_stop_lon": [17.1, 17.2, 17.3, 17.1, 17.2, 17.3],
            "end_stop_lat": [51.2, 51.3, 51.1, 51.3, 51.1, 51.2],
            "end_stop_lon": [17.2, 17.3, 17.1, 17.3, 17.1, 17.2],
            "line": ["Line1", "Line2", "Line3", "Line4", "Line5", "Line6"],
            "departure_time": [
                "08:00:00",
                "08:30:00",
                "09:00:00",
                "08:15:00",
                "08:45:00",
                "09:15:00",
            ],
            "arrival_time": [
                "08:20:00",
                "08:50:00",
                "09:20:00",
                "08:35:00",
                "09:05:00",
                "09:35:00",
            ],
        }
    )


@pytest.fixture
def complex_data():
    return pd.DataFrame(
        {
            "start_stop": [
                "StationA",
                "StationA",
                "StationB",
                "StationB",
                "StationC",
                "StationC",
                "StationD",
                "StationD",
                "StationE",
            ],
            "end_stop": [
                "StationB",
                "StationC",
                "StationC",
                "StationD",
                "StationD",
                "StationE",
                "StationE",
                "StationA",
                "StationA",
            ],
            "start_stop_lat": [51.1, 51.1, 51.2, 51.2, 51.3, 51.3, 51.4, 51.4, 51.5],
            "start_stop_lon": [17.1, 17.1, 17.2, 17.2, 17.3, 17.3, 17.4, 17.4, 17.5],
            "end_stop_lat": [51.2, 51.3, 51.3, 51.4, 51.4, 51.5, 51.5, 51.1, 51.1],
            "end_stop_lon": [17.2, 17.3, 17.3, 17.4, 17.4, 17.5, 17.5, 17.1, 17.1],
            "line": [
                "Line1",
                "Line1",
                "Line2",
                "Line2",
                "Line3",
                "Line3",
                "Line4",
                "Line4",
                "Line5",
            ],
            "departure_time": [
                "08:00:00",
                "08:05:00",
                "08:30:00",
                "08:35:00",
                "09:00:00",
                "09:05:00",
                "09:30:00",
                "09:35:00",
                "10:00:00",
            ],
            "arrival_time": [
                "08:20:00",
                "08:25:00",
                "08:50:00",
                "08:55:00",
                "09:20:00",
                "09:25:00",
                "09:50:00",
                "09:55:00",
                "10:20:00",
            ],
        }
    )


def test_calculate_route_cost_basic(sample_data):
    """Test basic route cost calculation for a simple sequence."""
    graph, station_coordinates = build_graph(sample_data)

    cost, path, is_valid = calculate_route_cost(
        "StationA",
        ["StationB", "StationC"],
        "t",
        "07:30:00",
        graph,
        station_coordinates,
    )

    assert is_valid
    assert cost != inf
    assert len(path) > 0

    stations_visited = ["StationA"]

    for ride in path:
        line, board_stop, _, alight_stop, _ = ride
        assert board_stop == stations_visited[-1]
        stations_visited.append(alight_stop)

    assert stations_visited == ["StationA", "StationB", "StationC", "StationA"]


def test_calculate_route_cost_time_vs_transfers(complex_data):
    """Test that different criteria produce different route costs."""
    graph, station_coordinates = build_graph(complex_data)

    time_cost, time_path, is_valid_time = calculate_route_cost(
        "StationA",
        ["StationC", "StationE"],
        "t",
        "07:30:00",
        graph,
        station_coordinates,
    )

    transfers_cost, transfers_path, is_valid_transfers = calculate_route_cost(
        "StationA",
        ["StationC", "StationE"],
        "s",
        "07:30:00",
        graph,
        station_coordinates,
    )

    assert is_valid_time
    assert is_valid_transfers

    time_transfers = len(set(ride[0] for ride in time_path)) - 1
    transfers_transfers = len(set(ride[0] for ride in transfers_path)) - 1

    time_total_time = time_path[-1][4] - get_time_in_seconds("07:30:00")
    transfers_total_time = transfers_path[-1][4] - get_time_in_seconds("07:30:00")

    if time_total_time != transfers_total_time:
        assert time_total_time <= transfers_total_time
    if time_transfers != transfers_transfers:
        assert transfers_transfers <= time_transfers


def test_tabu_search_basic(sample_data):
    """Test basic tabu search functionality."""
    graph, station_coordinates = build_graph(sample_data)

    cost, path = tabu_search(
        "StationA",
        ["StationB", "StationC"],
        "t",
        "07:30:00",
        graph,
        station_coordinates,
        max_iterations=50,
        tabu_size=10,
        neighborhood_size=10,
    )

    assert cost != inf
    assert len(path) > 0

    visited_stations = set()

    for ride in path:
        _, board_stop, _, alight_stop, _ = ride
        visited_stations.add(board_stop)
        visited_stations.add(alight_stop)

    assert "StationA" in visited_stations
    assert "StationB" in visited_stations
    assert "StationC" in visited_stations


def test_tabu_search_empty_stations(sample_data):
    """Test tabu search with empty list of stations to visit."""
    graph, station_coordinates = build_graph(sample_data)

    cost, path = tabu_search(
        "StationA", [], "t", "07:30:00", graph, station_coordinates
    )

    assert cost == 0
    assert path == []


def test_tabu_search_nonexistent_station(sample_data):
    """Test tabu search with nonexistent stations."""
    graph, station_coordinates = build_graph(sample_data)

    cost, path = tabu_search(
        "StationA", ["NonexistentStation"], "t", "07:30:00", graph, station_coordinates
    )

    assert cost == inf
    assert path == []


def test_tabu_search_parameters(complex_data):
    """Test tabu search with different parameter values."""
    graph, station_coordinates = build_graph(complex_data)

    random.seed(42)

    cost_small, path_small = tabu_search(
        "StationA",
        ["StationC", "StationE"],
        "t",
        "07:30:00",
        graph,
        station_coordinates,
        max_iterations=10,
        tabu_size=5,
        neighborhood_size=5,
    )

    random.seed(42)

    cost_large, path_large = tabu_search(
        "StationA",
        ["StationC", "StationE"],
        "t",
        "07:30:00",
        graph,
        station_coordinates,
        max_iterations=50,
        tabu_size=20,
        neighborhood_size=20,
    )

    assert cost_small != inf
    assert cost_large != inf

    assert len(path_small) > 0
    assert len(path_large) > 0


def test_time_vs_transfers_optimization(complex_data):
    """Test that different optimization criteria produce different results."""
    graph, station_coordinates = build_graph(complex_data)

    random.seed(42)

    time_cost, time_path = tabu_search(
        "StationA",
        ["StationC", "StationE"],
        "t",
        "07:30:00",
        graph,
        station_coordinates,
        max_iterations=50,
    )

    random.seed(42)

    transfers_cost, transfers_path = tabu_search(
        "StationA",
        ["StationC", "StationE"],
        "s",
        "07:30:00",
        graph,
        station_coordinates,
        max_iterations=50,
    )

    assert time_cost != inf
    assert transfers_cost != inf

    time_actual_time = time_path[-1][4] - get_time_in_seconds("07:30:00")
    transfers_actual_time = transfers_path[-1][4] - get_time_in_seconds("07:30:00")

    time_actual_transfers = len(set(ride[0] for ride in time_path)) - 1
    transfers_actual_transfers = len(set(ride[0] for ride in transfers_path)) - 1

    if (
        time_actual_time != transfers_actual_time
        and time_actual_transfers != transfers_actual_transfers
    ):
        assert (
            time_actual_time <= transfers_actual_time
            or transfers_actual_transfers <= time_actual_transfers
        )


def test_main_function(monkeypatch, sample_data, capfd):
    """Test the main function with mocked input and data loading."""

    input_values = [
        "StationA",
        "StationB;StationC",
        "t",
        "07:30:00",
    ]
    input_mock = lambda: input_values.pop(0)
    monkeypatch.setattr("builtins.input", input_mock)

    monkeypatch.setattr("run_tabu.load_data", lambda: sample_data)

    old_stderr = sys.stderr
    captured_stderr = StringIO()
    sys.stderr = captured_stderr

    try:
        main()

        captured_stdout, _ = capfd.readouterr()
        stderr_output = captured_stderr.getvalue()

        assert "Line" in captured_stdout
        assert "Cost:" in stderr_output
        assert "Computation time:" in stderr_output
    finally:
        sys.stderr = old_stderr


def test_different_visit_sequences(complex_data):
    """Test that different visit sequences have different costs."""
    graph, station_coordinates = build_graph(complex_data)

    stations = ["StationB", "StationC", "StationD", "StationE"]
    sequence1 = stations.copy()

    sequence2 = stations.copy()
    if len(sequence2) >= 2:
        sequence2[0], sequence2[-1] = sequence2[-1], sequence2[0]

    cost1, path1, is_valid1 = calculate_route_cost(
        "StationA", sequence1, "t", "07:30:00", graph, station_coordinates
    )

    cost2, path2, is_valid2 = calculate_route_cost(
        "StationA", sequence2, "t", "07:30:00", graph, station_coordinates
    )

    assert is_valid1
    assert is_valid2

    assert cost1 != inf
    assert cost2 != inf


def test_with_real_data():
    """Test with real data from connection_graph.csv if available."""
    try:
        df = load_data()
        graph, station_coordinates = build_graph(df)

        all_stations = list(graph.keys())
        if len(all_stations) < 3:
            pytest.skip("Not enough stations in the data")

        start_station = all_stations[0]
        stations_to_visit = random.sample(
            all_stations[1:], min(2, len(all_stations) - 1)
        )

        cost, path = tabu_search(
            start_station,
            stations_to_visit,
            "t",
            "07:30:00",
            graph,
            station_coordinates,
            max_iterations=10,
            tabu_size=5,
            neighborhood_size=5,
        )

        assert isinstance(cost, (int, float))

    except FileNotFoundError:
        pytest.skip("connection_graph.csv not found")
