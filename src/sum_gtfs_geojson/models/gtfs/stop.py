from pydantic import Field, HttpUrl, constr
from typing import Optional
from .. import SumGtfsBaseModel


class Stop(SumGtfsBaseModel):
    """
    Represents a physical location where passengers board or alight from vehicles.

    Attributes:
        stop_id: Unique identifier for the stop.
        stop_name: Name of the stop.
        stop_desc: Description of the stop.
        stop_lat: Latitude of the stop.
        stop_lon: Longitude of the stop.
        zone_id: Identifier for fare zone.
        stop_url: URL with stop information.
        location_type: Indicates if it's a stop or station.
        parent_station: Identifier for parent station (if nested).
    """
    stop_id: str
    stop_name: str
    stop_desc: Optional[str] = Field(default=None)
    stop_lat: float
    stop_lon: float
    zone_id: Optional[str] = Field(default=None)
    stop_url: Optional[str] = Field(default=None)
    location_type: Optional[int] = Field(default=0)  # 0 = stop, 1 = station
    parent_station: Optional[str] = Field(default=None)
