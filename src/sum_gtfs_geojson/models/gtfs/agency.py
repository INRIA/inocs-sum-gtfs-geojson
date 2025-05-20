from pydantic import Field, HttpUrl, constr
from typing import Optional
from .. import SumGtfsBaseModel


class Agency(SumGtfsBaseModel):
    """
    Represents a public transport agency that provides transit services.

    Attributes:
        agency_id: Unique identifier for the agency (optional if only one agency).
        agency_name: Full name of the agency.
        agency_url: URL of the agency's website.
        agency_timezone: Timezone where the agency is located.
        agency_lang: Language used for text in the feed.
        agency_phone: A voice telephone number for the agency.
        agency_fare_url: URL of a web page with fare information.
    """
    agency_id: Optional[str] = Field(default=None)
    agency_name: str
    agency_url: str
    agency_timezone: str
    agency_lang: Optional[str] = Field(default=None)
    agency_phone: Optional[str] = Field(default=None)
    agency_fare_url: Optional[str] = Field(default=None)
