from typing import List
from shapely.geometry import Point, MultiPoint
import h3
from sum_gtfs_geojson.models import HexGrid, HexCell


class GeoToolkit:

    @staticmethod
    def generate_hex_grid(points: List[Point], resolution: int) -> HexGrid:
        """
        Generate a hexagonal grid that covers the area defined by the input Shapely Points.

        Args:
            points: A list of shapely.geometry.Point objects representing geolocations.
                    Points must be in WGS84 (lon, lat) format.
            resolution: H3 resolution level (int), where higher means finer grid.

        Returns:
            GeoDataFrame with one row per hex cell, including geometry and h3_id.
        """
        if not points:
            raise ValueError("Point list is empty")
        if resolution < 0 or resolution > 15:
            raise ValueError("Resolution must be between 0 and 15")

        multipoint = MultiPoint(points)
        convex_hull = multipoint.convex_hull
        buffered_polygon = convex_hull.buffer(0.01)

        coords = [(x, y) for x, y in buffered_polygon.exterior.coords]
        polygon = h3.LatLngPoly(coords)

        hex_ids = h3.polygon_to_cells(polygon, resolution)

        cells = []
        for h3_id in hex_ids:
            lat, lon = h3.cell_to_latlng(h3_id)
            center = (lon, lat)
            boundary = h3.cell_to_boundary(h3_id)
            polygon = [(point[0], point[1]) for point in boundary]
            cells.append(HexCell(h3_id=h3_id, center=center, polygon=polygon))

        return HexGrid(resolution=resolution, cells=cells)
