from typing import Optional
from pydantic import Field
from .. import SumGtfsBaseModel

class StopTime(SumGtfsBaseModel):
    """
    Represents a single stop time for a trip in the GTFS feed.

    Attributes:
        trip_id: Identifier for the trip.
        arrival_time: Scheduled arrival time at the stop (HH:MM:SS).
        departure_time: Scheduled departure time from the stop (HH:MM:SS).
        stop_id: Identifier for the stop.
        stop_sequence: Order of the stop for the trip.
        stop_headsign: (Optional) Text shown to riders about the stop.
        pickup_type: (Optional) Pickup method (0=regular, 1=none, etc.).
        drop_off_type: (Optional) Drop-off method (0=regular, 1=none, etc.).
        shape_dist_traveled: (Optional) Distance traveled along the shape to this stop.
        timepoint: (Optional) Indicates if the time is exact or approximate.
    """
    trip_id: str
    arrival_time: str
    departure_time: str
    stop_id: str
    stop_sequence: int
    stop_headsign: Optional[str] = Field(default=None)
    pickup_type: Optional[int] = Field(default=None)
    drop_off_type: Optional[int] = Field(default=None)
    shape_dist_traveled: Optional[float] = Field(default=None)
    timepoint: Optional[int] = Field(default=None)