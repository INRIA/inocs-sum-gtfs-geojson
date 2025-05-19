from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from . import StationStatusPeriod, StationInfo


class StationInfoStatus(StationInfo):
    """
    Represents the time series of status observations for a single bike station.

    This model is useful for tracking how bike and dock availability changes over time
    at a specific station. It supports analysis of temporal patterns, station reliability,
    and peak usage periods.

    Attributes:
        station_id (str): Unique identifier for the station.
        history (List[StationStatusPeriod]): Chronologically ordered list of status snapshots
            representing the station's inventory (bikes/docks) over periods of time.
    """
    history: List[StationStatusPeriod] = Field(..., description="List of status records over periods of time.")
