from .. import SumGtfsBaseModel
from pydantic import Field
from typing import List, Tuple


class HexCell(SumGtfsBaseModel):
    h3_id: str = Field(..., description="Unique H3 cell identifier")
    center: Tuple[float, float] = Field(..., description="Center point of the hex cell as (longitude, latitude)")
    polygon: List[Tuple[float, float]] = Field(..., description="List of (longitude, latitude) tuples defining the hexagon boundary")
