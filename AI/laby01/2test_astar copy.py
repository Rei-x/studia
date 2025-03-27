from math import inf
import pytest
import pandas as pd
from astar_time_przesiadki import (
    build_graph,
    when_to_ride,
)
from utils import format_time, get_time_in_seconds


# Sample test data - minimal connections for testing
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


# More complex test data for testing different optimization criteria
@pytest.fixture
def complex_data():
    return pd.DataFrame(
        {
            # Direct but slow route from A to D
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
                "Line1",  # Direct but slow A->D
                "Line2",  # A->B
                "Line2",  # B->C
                "Line3",  # B->E
                "Line3",  # C->D - faster multi-line route
                "Line3",  # E->F
                "Line4",  # F->D
            ],
            "departure_time": [
                "09:00:00",  # Direct A->D (slow)
                "08:00:00",  # A->B
                "08:30:00",  # B->C
                "08:35:00",  # B->E
                "08:50:00",  # C->D (fast path component)
                "09:10:00",  # E->F
                "09:30:00",  # F->D
            ],
            "arrival_time": [
                "10:00:00",  # Direct A->D (slow) - 1 hour
                "08:20:00",  # A->B
                "08:45:00",  # B->C
                "08:50:00",  # B->E
                "09:05:00",  # C->D (fast path component)
                "09:20:00",  # E->F
                "09:45:00",  # F->D
            ],
        }
    )


def test_time_conversion():
    """Test time conversion functions"""
    assert get_time_in_seconds("01:30:45") == 5445
    assert format_time(5445) == "01:30:45"


# def test_station_extraction(sample_data):
#     """Test extraction of unique stations"""
#     stations = get_unique_stations(sample_data)
#     assert set(stations) == {"StationA", "StationB", "StationC"}


# def test_coordinates_extraction(sample_data):
#     """Test extraction of station coordinates"""
#     stations = get_unique_stations(sample_data)
#     coords = extract_station_coordinates(sample_data, stations)
#     assert coords["StationA"] == (51.1, 17.1)
#     assert coords["StationB"] == (51.2, 17.2)
#     assert coords["StationC"] == (51.3, 17.3)


def test_simple_route(sample_data):
    """Test finding a route in the sample data"""

    # Find route from A to C
    result_time, path = when_to_ride(
        "StationA", "StationC", "t", "07:45:00", graph=build_graph(sample_data)
    )

    assert result_time != inf
    assert len(path) > 0
    # Can add more assertions based on expected results


def test_time_optimization(complex_data):
    """Test that time optimization works correctly"""

    # Find fastest route from A to D
    result_time, path = when_to_ride(
        "StationA",
        "StationD",
        "t",  # optimize for time
        "07:45:00",
        graph=build_graph(complex_data),
    )

    # With time optimization, we expect to get the fastest route
    assert result_time != inf
    assert len(path) > 0

    # Get the complete path through the graph
    lines_used = [ride[0] for ride in path]

    # Ensure we found a path
    assert len(lines_used) == 3


def test_transfers_optimization(complex_data):
    """Test that transfers optimization works correctly"""

    # Find route with fewest transfers from A to D
    result_time, path = when_to_ride(
        "StationA",
        "StationD",
        "s",  # optimize for transfers
        "07:45:00",
        graph=build_graph(complex_data),
    )

    # With transfers optimization, we expect to get the route with fewest transfers
    # even if it takes longer
    assert result_time != inf
    assert len(path) > 0

    # Get the lines used in the path
    lines_used = set(ride[0] for ride in path)

    # For this test data, the single-transfer route should be preferred
    assert len(lines_used) <= 1  # We expect at most 1 different lines


def test_comparison_of_optimizations(complex_data):
    """Test that different optimization criteria give different results when appropriate"""

    # Get time-optimized route
    time_result, time_path = when_to_ride(
        "StationA", "StationD", "t", "07:45:00", graph=build_graph(complex_data)
    )

    # Get transfers-optimized route
    transfers_result, transfers_path = when_to_ride(
        "StationA", "StationD", "s", "07:45:00", graph=build_graph(complex_data)
    )

    print("a", time_path, "b", transfers_path)

    # Both routes should be valid
    assert time_result != inf
    assert transfers_result != inf

    # Get number of transfers for each route
    time_transfers = (
        len(set(ride[0] for ride in time_path)) - 1
    )  # -1 because n lines means n-1 transfers
    transfers_transfers = len(set(ride[0] for ride in transfers_path)) - 1

    # In our test data, we designed it so that:
    # - Either the time-optimized route takes less time but has more transfers
    # - Or the results are identical (in which case both methods should find the same optimal route)

    if time_result != transfers_result:
        # If results differ, time-optimized should be faster
        assert time_result < transfers_result
        # And transfer-optimized should have fewer transfers
        assert transfers_transfers <= time_transfers


def test_no_route(sample_data):
    """Test when there is no valid route"""

    # Try to find a route to a non-existent station
    result_time, path = when_to_ride(
        "StationA",
        "NonExistentStation",
        "t",
        "07:45:00",
        graph=build_graph(sample_data),
    )

    assert result_time == inf
    assert len(path) == 0
