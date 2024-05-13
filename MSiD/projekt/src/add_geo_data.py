from geopy.distance import distance
from geopy.geocoders import Nominatim
from geopy.geocoders.databc import Location

selfhosted_nominatim = Nominatim(
    user_agent="msid_project", scheme="http", domain="localhost:8080"
)
centre: Location = selfhosted_nominatim.geocode("Galeria Dominikańska, Wrocław")  # type: ignore
centre_point = (centre.latitude, centre.longitude)


def add_location_add_distance_to_city_centre(row):
    location: Location = selfhosted_nominatim.geocode(row["fullLocation"])  # type: ignore

    if location is None:
        return row

    location_point = (location.latitude, location.longitude)
    row["distanceToCityCentre"] = distance(centre_point, location_point).m
    row["latitude"] = location_point[0]
    row["longitude"] = location_point[1]
    row["address"] = location.address

    return row
