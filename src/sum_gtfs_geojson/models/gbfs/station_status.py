from .. import SumGtfsBaseModel


class StationStatus(SumGtfsBaseModel):
    """
    Real-time status of a single bike station.

    Attributes:
        station_id (str): ID of the station matching the station_information feed.
        num_bikes_available (int): Number of bikes available for rent.
        num_docks_available (int): Number of empty docks for returning bikes.
        is_installed (int): 1 if the station is installed, 0 otherwise.
        is_renting (int): 1 if the station is allowing rentals, 0 otherwise.
        is_returning (int): 1 if the station is allowing returns, 0 otherwise.
        last_reported (int): Last time the station was reported, in Unix timestamp.
    """
    station_id: str
    num_bikes_available: int
    num_docks_available: int
    is_installed: int
    is_renting: int
    is_returning: int
    last_reported: int
