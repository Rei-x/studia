from math import inf
import pytest
import pandas as pd
from astar_time_przesiadki import (
    build_graph,
    when_to_ride,
)
from utils import format_time, get_time_in_seconds


@pytest.fixture
def sample_data():
    return pd.DataFrame(
        {
            "start_stop": ["StationA", "StationB", "StationA"],
            "end_stop": ["StationB", "StationC", "StationC"],
            "start_stop_lat": [51.1, 51.2, 51.1],
            "start_stop_lon": [17.1, 17.2, 17.1],
            "end_stop_lat": [51.2, 51.3, 51.3],
            "end_stop_lon": [17.2, 17.3, 17.3],
            "line": ["Line1", "Line2", "Line3"],
            "departure_time": ["08:00:00", "08:30:00", "08:15:00"],
            "arrival_time": ["08:20:00", "08:45:00", "08:40:00"],
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
                "StationE",
                "StationF",
            ],
            "end_stop": [
                "StationD",
                "StationB",
                "StationC",
                "StationE",
                "StationD",
                "StationF",
                "StationD",
            ],
            "start_stop_lat": [51.1, 51.1, 51.2, 51.2, 51.3, 51.5, 51.6],
            "start_stop_lon": [17.1, 17.1, 17.2, 17.2, 17.3, 17.5, 17.6],
            "end_stop_lat": [51.4, 51.2, 51.3, 51.5, 51.4, 51.6, 51.4],
            "end_stop_lon": [17.4, 17.2, 17.3, 17.5, 17.4, 17.6, 17.4],
            "line": [
                "Line1",
                "Line2",
                "Line2",
                "Line3",
                "Line3",
                "Line3",
                "Line4",
            ],
            "departure_time": [
                "09:00:00",
                "08:00:00",
                "08:30:00",
                "08:35:00",
                "08:50:00",
                "09:10:00",
                "09:30:00",
            ],
            "arrival_time": [
                "10:00:00",
                "08:20:00",
                "08:45:00",
                "08:50:00",
                "09:05:00",
                "09:20:00",
                "09:45:00",
            ],
        }
    )


def test_time_conversion():
    """Test time conversion functions"""
    assert get_time_in_seconds("01:30:45") == 5445
    assert format_time(5445) == "01:30:45"


def test_simple_route(sample_data):
    """Test finding a route in the sample data"""
    graph, station_coordinates = build_graph(sample_data)

    result_time, path = when_to_ride(
        "StationA",
        "StationC",
        "t",
        "07:45:00",
        graph=graph,
        station_coordinates=station_coordinates,
    )

    assert result_time != inf
    assert len(path) > 0


def test_time_optimization(complex_data):
    """Test that time optimization works correctly"""
    graph, station_coordinates = build_graph(complex_data)

    result_time, path = when_to_ride(
        "StationA",
        "StationD",
        "t",
        "07:45:00",
        graph=graph,
        station_coordinates=station_coordinates,
    )

    assert result_time != inf
    assert len(path) > 0

    lines_used = [ride[0] for ride in path]

    assert len(lines_used) == 3


def test_transfers_optimization(complex_data):
    """Test that transfers optimization works correctly"""
    graph, station_coordinates = build_graph(complex_data)

    result_time, path = when_to_ride(
        "StationA",
        "StationD",
        "s",
        "07:45:00",
        graph=graph,
        station_coordinates=station_coordinates,
    )

    assert result_time != inf
    assert len(path) > 0

    lines_used = set(ride[0] for ride in path)

    assert len(lines_used) <= 1


def test_comparison_of_optimizations(complex_data):
    """Test that different optimization criteria give different results when appropriate"""

    graph, station_coordinates = build_graph(complex_data)

    time_result, time_path = when_to_ride(
        "StationA",
        "StationD",
        "t",
        "07:45:00",
        graph=graph,
        station_coordinates=station_coordinates,
    )

    transfers_result, transfers_path = when_to_ride(
        "StationA",
        "StationD",
        "s",
        "07:45:00",
        graph=graph,
        station_coordinates=station_coordinates,
    )

    print("a", time_path, "b", transfers_path)

    assert time_result != inf
    assert transfers_result != inf

    time_transfers = len(set(ride[0] for ride in time_path)) - 1
    transfers_transfers = len(set(ride[0] for ride in transfers_path)) - 1

    if time_result != transfers_result:
        assert time_result < transfers_result

        assert transfers_transfers <= time_transfers


def test_no_route(sample_data):
    """Test when there is no valid route"""
    graph, station_coordinates = build_graph(sample_data)

    result_time, path = when_to_ride(
        "StationA",
        "NonExistentStation",
        "t",
        "07:45:00",
        graph=graph,
        station_coordinates=station_coordinates,
    )

    assert result_time == inf
    assert len(path) == 0
