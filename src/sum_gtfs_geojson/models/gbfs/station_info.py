from pydantic import Field
from typing import List, Optional
from .. import SumGtfsBaseModel


class StationInfo(SumGtfsBaseModel):
    """
    Static information about a single bike station in the system.

    Attributes:
        station_id (str): Unique identifier for the station.
        name (str): Public-facing name of the station.
        short_name (Optional[str]): Short or code name (e.g., for internal use or maps).
        lat (float): Latitude coordinate of the station.
        lon (float): Longitude coordinate of the station.
        address (Optional[str]): Physical address of the station.
        capacity (Optional[int]): Total number of docks at the station.
        region_id (Optional[str]): Region identifier, if the system uses administrative regions.
        rental_methods (Optional[List[str]]): Accepted rental methods (e.g., "key", "app").
        has_kiosk (Optional[bool]): Whether the station has an on-site kiosk.
    """
    station_id: str
    name: str
    short_name: Optional[str] = None
    lat: float
    lon: float
    address: Optional[str] = None
    capacity: Optional[int] = None
    region_id: Optional[str] = None
    rental_methods: Optional[List[str]] = None
    has_kiosk: Optional[bool] = None
