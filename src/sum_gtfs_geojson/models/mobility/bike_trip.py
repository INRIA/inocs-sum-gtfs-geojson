from datetime import datetime
from .. import SumGtfsBaseModel
from pydantic import field_validator


class BikeTrip(SumGtfsBaseModel):
    """
    Represents a single bike-sharing trip made by a user or rental.

    This model captures trip-level data including timestamps, GPS locations,
    distance, and vehicle type. It is typically used for micromobility analysis,
    demand modeling, or origin-destination mapping.

    Attributes:
        trip_id (str): Unique identifier for the trip.
        rental_id (str): Identifier of the rental transaction (may differ from trip_id).
        vehicle_type (str): Type of vehicle used (e.g., "bike", "e-bike", "scooter").
        trip_started_at_utc (datetime): UTC timestamp when the trip began.
        trip_ended_at_utc (datetime): UTC timestamp when the trip ended.
        latitude_start (float): Latitude of the trip origin.
        longitude_start (float): Longitude of the trip origin.
        latitude_end (float): Latitude of the trip destination.
        longitude_end (float): Longitude of the trip destination.
        distance_in_km (float): Distance traveled during the trip in kilometers.
    """

    trip_id: str
    rental_id: str
    vehicle_type: str
    trip_started_at_utc: datetime
    trip_ended_at_utc: datetime
    latitude_start: float
    longitude_start: float
    latitude_end: float
    longitude_end: float
    distance_in_km: float

    @field_validator("trip_started_at_utc", mode="before")
    def parse_trip_start(cls, value):
        if isinstance(value, str) and value.endswith(" UTC"):
            value = value.replace(" UTC", "")
        return datetime.fromisoformat(value)

    @field_validator("trip_ended_at_utc", mode="before")
    def parse_trip_end(cls, value):
        if isinstance(value, str) and value.endswith(" UTC"):
            value = value.replace(" UTC", "")
        return datetime.fromisoformat(value)
