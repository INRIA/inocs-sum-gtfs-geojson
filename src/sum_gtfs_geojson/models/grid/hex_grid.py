from shapely.geometry import Point, Polygon
import geopandas as gpd
import h3
from typing import List, Optional
from .. import SumGtfsBaseModel
from .hex_cell import HexCell
from pydantic import Field



class HexGrid(SumGtfsBaseModel):
    resolution: int = Field(..., description="H3 resolution level")
    cells: List[HexCell] = Field(..., description="List of hexagonal cells")
    
    @classmethod
    def from_geodataframe(cls, gdf: gpd.GeoDataFrame, resolution: int) -> "HexGrid":
        """
        Create a HexGrid instance from a GeoDataFrame of point geometries.

        Args:
            gdf: GeoDataFrame containing point geometries.
            resolution: H3 resolution level.

        Returns:
            HexGrid instance.
        """
        if gdf.empty:
            raise ValueError("The GeoDataFrame is empty.")
        
        print('Generating hex grid, gdf containts h3 ids:', gdf['h3_id'].unique())
        print('grid contains the following geometries:', gdf['geometry'].count())

        # Create a bounding polygon (convex hull with a small buffer)
        bounding_polygon = gdf.unary_union.convex_hull.buffer(0.01)  # ~1km buffer

        # Generate H3 cell indices covering the bounding polygon
        hex_ids = h3.polyfill(bounding_polygon.__geo_interface__, resolution)

        # Create HexCell instances
        cells = []
        for h3_id in hex_ids:
            lat, lon = h3.cell_to_latlng(h3_id)
            center = (lon, lat)
            boundary = h3.cell_to_boundary(h3_id)
            polygon = [(point[0], point[1]) for point in boundary]
            cells.append(HexCell(h3_id=h3_id, center=center, polygon=polygon))

        return cls(resolution=resolution, cells=cells)

    def to_geodataframe(self) -> gpd.GeoDataFrame:
        """
        Convert the HexGrid instance to a GeoDataFrame.

        Returns:
            GeoDataFrame with hex cell geometries and identifiers.
        """
        hex_ids = [cell.h3_id for cell in self.cells]
        polygons = [Polygon(cell.polygon) for cell in self.cells]
        gdf = gpd.GeoDataFrame({"h3_id": hex_ids, "geometry": polygons}, crs="EPSG:4326")
        return gdf

    def to_geojson(self, filepath: str = None) -> dict:
        """Export the grid to a GeoJSON file."""
        
        gdf = self.to_geodataframe()
        if filepath is not None:
            gdf.to_file(filepath, driver="GeoJSON")
        
        return gdf.to_json()