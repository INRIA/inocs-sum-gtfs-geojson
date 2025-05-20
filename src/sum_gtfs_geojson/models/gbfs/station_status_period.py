from pydantic import Field
from datetime import datetime
from typing import Optional

from . import StationStatus  # Adjust import as needed


class StationStatusPeriod(StationStatus):
    """
    Extends StationStatus with period metadata to group availability by time periods.

    This is useful for analyzing patterns across predefined time windows (e.g., by hour,
    weekday/weekend, or month).

    Attributes:
        period_id (str): Identifier for the time period (e.g., "weekday_morning", "2024-05").
        period_label (Optional[str]): Human-readable label for the time period.
    """
    period_id: str = Field(...,
                           description="Machine-readable identifier for the analysis period.")
    period_label: Optional[str] = Field(
        default=None, description="Display name for the period (e.g., 'Weekday Morning').")
