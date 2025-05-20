from pydantic import Field
from .. import SumGtfsBaseModel


class Ridership(SumGtfsBaseModel):
    """
    Represents passenger activity data at a specific transit stop and time slot.

    This model captures detailed ridership metrics, including boardings and alightings,
    along with contextual information like the line, stop location, time, and whether
    the data is filtered or finalized. It can be used for operational analysis, planning,
    or visualization of public transit usage patterns.

    Attributes:
        date (str): Date of observation in YYYY-MM-DD format.
        timeslot (str): Time window when the observation was made (e.g., "07:00-08:00").
        day_index (int): Index of the day in the week (e.g., 1 for Monday, 7 for Sunday).
        line_type (str): Category or type of the transit line (e.g., metro, bus, tram).
        schedule_type (str): Type of schedule active on the observation day (e.g., "holiday", "regular").
        line (str): Name or identifier of the transit line.
        stop_name (str): Common name of the transit stop.
        stop_code (str): Unique or long code identifier for the stop.
        boardings (int): Number of passengers boarding the vehicle at this stop during the time slot.
        alightings (int): Number of passengers alighting from the vehicle at this stop during the time slot.
        day_label (str): Label for the day of the week (e.g., "Monday", "Friday").
        week_index (int): Index of the week within the dataset or calendar year.
        month_year (str): Month and year of the observation (e.g., "2024-05").
        stop_lat (float): Latitude coordinate of the stop.
        stop_lon (float): Longitude coordinate of the stop.
        is_final (bool): Flag indicating whether the data is final and validated.
        is_filtered (bool): Flag indicating whether this record was excluded from primary analysis (e.g., due to quality filters).
    """

    date: str
    timeslot: str
    day_index: int
    line_type: str
    schedule_type: str
    line: str
    stop_name: str
    stop_code: str
    boardings: int
    alightings: int
    day_label: str
    week_index: int
    month_year: str
    stop_lat: float
    stop_lon: float
    is_final: bool
    is_filtered: bool
