from pydantic import  Field, HttpUrl, constr
from typing import Optional
from .. import SumGtfsBaseModel

class Route(SumGtfsBaseModel):
    """
    Describes a route for transit services (e.g., bus, train, subway).

    Attributes:
        route_id: Unique identifier for the route.
        agency_id: Identifies the agency for the route.
        route_short_name: Short name used in signs and schedules.
        route_long_name: Descriptive name of the route.
        route_desc: Description of the route.
        route_type: Type of transportation used.
        route_url: URL with information about the route.
        route_color: Color used to display the route on a map.
        route_text_color: Text color used on signage.
    """
    route_id: str
    agency_id: Optional[str] = Field(default=None)
    route_short_name: str
    route_long_name: str
    route_desc: Optional[str] = Field(default=None)
    route_type: int
    route_url: Optional[str] = Field(default=None)
    route_color: Optional[str] = Field(default=None)
    route_text_color: Optional[str] = Field(default=None)
