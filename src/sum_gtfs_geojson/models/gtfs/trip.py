from pydantic import Field, HttpUrl, constr
from typing import Optional
from .. import SumGtfsBaseModel


class Trip(SumGtfsBaseModel):
    """
    Defines a trip: a sequence of two or more stops with scheduled times.

    Attributes:
        route_id: Identifier for the route this trip belongs to.
        service_id: Identifier for the service schedule.
        trip_id: Unique identifier for the trip.
        trip_headsign: Text shown to riders describing trip destination.
        trip_short_name: Public-facing identifier for the trip.
        direction_id: Indicates travel direction (0 or 1).
        block_id: Identifies a block of sequential trips.
        shape_id: Identifies the shape used to draw the route.
    """
    route_id: Optional[str] = Field(default=None)
    service_id: Optional[str] = Field(default=None)
    trip_id: Optional[str] = Field(default=None)
    trip_headsign: Optional[str] = Field(default=None)
    trip_short_name: Optional[str] = Field(default=None)
    direction_id: Optional[int] = Field(default=None)
    block_id: Optional[str] = Field(default=None)
    shape_id: Optional[str] = Field(default=None)
