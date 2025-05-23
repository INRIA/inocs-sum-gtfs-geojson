from pydantic import Field
from typing import Optional, List
from .. import SumGtfsBaseModel
from . import Stop


class Itinerary(SumGtfsBaseModel):
    """
    Represents a transit itinerary derived from GTFS data, encapsulating a sequence of stops for a specific trip along with associated route and trip metadata.

    Attributes:
        route_id (str): Unique identifier for the route.
        direction_id (int): Direction of travel for the trip; typically 0 or 1.
        trip_id (str): Unique identifier for the trip.
        headsign (Optional[str]): Text that appears on signage to identify the trip's destination or direction.
        route_short_name (Optional[str]): Short name of the route, often used in signage.
        route_long_name (Optional[str]): Full name of the route, providing more descriptive information.
        route_type (Optional[int]): Type of transportation used on the route (e.g., bus, tram, subway).
        color (Optional[str]): Route color designation, typically used in maps and signage.
        text_color (Optional[str]): Text color used in signage for the route.
        stops (List[Stop]): Ordered list of stops that the trip visits.
    """

    route_id: str = Field(..., description="Unique identifier for the route.")
    direction_id: int = Field(..., description="Direction of travel for the trip; typically 0 or 1.")
    trip_id: str = Field(..., description="Unique identifier for the trip.")
    headsign: Optional[str] = Field(default=None, description="Text that appears on signage to identify the trip's destination or direction.")
    route_short_name: Optional[str] = Field(default=None, description="Short name of the route, often used in signage.")
    route_long_name: Optional[str] = Field(default=None, description="Full name of the route, providing more descriptive information.")
    route_type: Optional[int] = Field(default=None, description="Type of transportation used on the route (e.g., bus, tram, subway).")
    color: Optional[str] = Field(default=None, description="Route color designation, typically used in maps and signage.")
    text_color: Optional[str] = Field(default=None, description="Text color used in signage for the route.")
    stops: List[Stop] = Field(..., description="Ordered list of stops that the trip visits.")